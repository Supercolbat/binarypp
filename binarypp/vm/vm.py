import io
import os.path
from argparse import Namespace
from sys import stdin, stdout
from typing import Any, List, Optional

import binarypp.logging as logging
import binarypp.parser as parser
from binarypp.types import Instruction, Marker, Pointer, String
from binarypp.vm.memory import Memory
from binarypp.vm.opcodes import *
from binarypp.vm.opmap import OP_MAP
from binarypp.vm.stack import Stack

# fmt: off
MODES = ["r", "r+", "rb", "rb+",  # 0000 - 0011
         "w", "w+", "wb", "wb+",  # 0100 - 0111
         "a", "a+", "ab", "ab+",  # 1000 - 1011
         "x", "x+", "xb", "xb+"]  # 1100 - 1111
# fmt: on


class VirtualMachine:
    def __init__(self, file: str, flags: Namespace):
        self.flags: Namespace = flags
        self.IP: Pointer = Pointer(0, -1)  # Instruction Pointer
        self.frames: List[Frame] = [Frame(file)]
        self.stack: Stack = Stack()

        self.last_goto: Pointer = Pointer(0, 0)

    def next_instruction(self) -> Optional[Instruction]:
        frame = self.frames[self.IP.frame]
        if self.IP.inst < frame.stream_size:
            self.IP.inst += 1
            return frame.stream[self.IP.inst]
        return None

    def main_loop(self, stream: List[Instruction]) -> None:
        self.frames[0].stream = stream
        self.frames[0].stream_size = len(stream) - 1

        self.initialize_markers(0)

        while True:
            inst = self.next_instruction()
            if inst is None:
                break

            frame: Frame = self.frames[self.IP.frame]

            if self.IP.inst > frame.target_IP:
                frame.target_IP = -1

            opcode = inst.opcode
            if frame.forwarded_args:
                args = frame.forwarded_args
                frame.forwarded_args = []
            else:
                args = inst.opargs

            if self.flags.step:
                print(
                    "\nInst: {} {} ({}){}".format(
                        OP_MAP[opcode],
                        args,
                        frame.forwarded_args,
                        f" {frame.target_IP - self.IP.inst}"
                        if frame.target_IP >= 0
                        else "",
                    )
                )

            if opcode == POP_STACK:
                """
                Pops one value from the stack

                PUSH_STACK 1
                POP_STACK
                """
                self.stack.pop()

            elif opcode == PUSH_STACK:
                """
                Pushes one value to the stack

                PUSH_STACK 1
                PUSH_STACK 2
                """
                self.stack.push(args[0])

            elif opcode == PUSH_STRING_STACK:
                """
                Pushes all codes as a string until a null-terminator is reached.

                PUSH_STRING_STACK Hello\0
                PUSH_STRING_STACK  world\0
                """
                self.stack.push(String(args))

            elif opcode == PUSH_LONG_STACK:
                """
                Pushes all codes as an int until a null-terminator is reached.

                PUSH_LONG_STACK 255 255 10\0
                """
                self.stack.push(sum(args))

            elif opcode == LOAD_MEMORY:
                """
                Pushes the value at the given memory address to the stack.
                0 is a reserved address.

                PUSH_STACK 5
                STORE_MEMORY 1
                LOAD_MEMORY 1
                LOAD_MEMORY 1
                BINARY_ADD
                """
                # print("loaded:", self.memory[args[0]])
                self.stack.push(frame.memory[args[0]])

            elif opcode == STORE_MEMORY:
                """
                Stores the top-most value in stack to the memory address.
                0 is a reserved address.

                PUSH_STACK 5
                STORE_MEMORY 1
                """
                frame.memory[args[0]] = self.stack.pop()

            elif opcode == DUP_TOP:
                """
                Duplicates the top-most stack value.

                PUSH_STACK 5
                DUP_TOP
                """
                val = self.stack.pop()
                self.stack.push(val)
                self.stack.push(val)

            # TODO: Include new READ_X_FROM instructions
            elif opcode == READ_FROM:
                """
                Reads values from a source until the terminator is reached (top stack).
                Pushes text to stack. Terminator is consumed but excluded.
                0 is stdin. Any other value is read from memory to determine source.

                PUSH_STACK \10
                READ_FROM 0 (stdin)
                PUSH_STRING_STACK "file.txt"
                OPEN_FILE 0
                STORE_MEMORY 1
                PUSH_STACK \32
                READ_FROM 1
                WRITE_TO 0 (stdin)
                """
                addr = args[0]
                terminator = chr(self.stack.pop())

                if addr == 0:
                    string = ""
                    while True:
                        ch = stdin.read(1)
                        if ch == terminator:
                            break
                        string += ch
                    self.stack.push(String(string))

                else:
                    fstream = frame.memory[addr]
                    if not isinstance(fstream, io.TextIOWrapper):
                        logging.error("MEMORY[{}] is not a file".format(addr))

                    string = ""
                    while True:
                        if (char := fstream.read(1)) == terminator or char != "":
                            break
                        string += char
                    self.stack.push(string)

            elif opcode == READ_CHAR_FROM:
                """
                Reads one char from a source. Pushes the char to stack.
                0 is stdin. Any other value is read from memory to determine source.

                READ_CHAR_FROM 0 (stdin)
                PUSH_STACK 48
                BINARY_SUBTRACT
                READ_CHAR_FROM 0 (stdin)
                BINARY_ADD
                WRITE_TO 0 (stdin)
                """
                addr = args[0]

                if addr == 0:
                    # self.stack.push(String(stdin.read(1)))
                    self.stack.push(ord(stdin.read(1)))
                else:
                    fstream = frame.memory[addr]
                    if not isinstance(stream, io.TextIOWrapper):
                        logging.error("MEMORY[{}] is not a file".format(addr))

                    self.stack.push(String(fstream.read(1)))

            elif opcode == WRITE_TO:
                """
                Writes the top-most stack to a source.
                0 is stdout. Any other value is reads from memory to determine source.
                """
                addr = args[0]
                if addr == 0:
                    content = self.stack.pop()
                    # print(content)
                    if isinstance(content, int):
                        stdout.write(chr(content))
                    else:
                        stdout.write(str(content))
                    stdout.flush()
                else:
                    fstream = frame.memory[addr]
                    if not isinstance(stream, io.TextIOWrapper):
                        logging.error("MEMORY[{}] is not a file".format(addr))

                    fstream.write(self.stack.pop())
                    self.stack.push(string)

            elif opcode == OPEN_FILE:
                """
                Opens file from stack and pushes it to stack.

                PUSH_STRING_STACK "file.txt"
                OPEN_FILE
                """
                mode = args[0]
                if 0b0000 <= mode <= 0b1111:
                    file = self.stack.pop()
                    # print(MODES[mode])
                    self.stack.push(open(file, MODES[mode]))
                else:
                    logging.error(
                        "Invalid file mode {}. Range: 0b0000-0b1111.".format(bin(mode))
                    )

            elif opcode == MAKE_MARKER:
                """
                Creates a marker at its current position in the code.
                Stores the marker at the given position in memory.

                MAKE_MARKER 1
                """
                frame.memory[args[0]] = Marker(self.IP)

            elif opcode == GOTO_MARKER:
                """
                Goes to the marker at the given memory address.

                MAKE_MARKER 1
                PUSH_STACK "Hello, world!\n"
                WRITE_TO 0
                GOTO_MARKER 2
                PUSH_STACK "This will never run"
                MAKE_MARKER 2
                GOTO_MARKER 1
                """
                if args[0] == 0:
                    self.IP.frame = self.last_goto.frame
                    self.IP.inst = self.last_goto.inst
                    continue

                target_marker = frame.memory[args[0]]
                if not isinstance(target_marker, Marker):
                    logging.error("Invalid marker at MEMORY[{}]".format(args[0]))

                self.last_goto.frame = self.IP.frame
                self.last_goto.inst = self.IP.inst
                self.IP.frame = target_marker.frame
                self.IP.inst = target_marker.inst

            #
            # Arithmetic
            #
            elif opcode == BINARY_ADD:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.push(a + b)

            elif opcode == BINARY_SUBTRACT:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.push(a - b)

            elif opcode == BINARY_MULTIPLY:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.push(a * b)

            elif opcode == BINARY_POWER:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.push(a**b)

            elif opcode == BINARY_TRUE_DIVIDE:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.push(a / b)

            elif opcode == BINARY_FLOOR_DIVIDE:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.push(int(a // b))

            elif opcode == BINARY_MODULO:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.push(a % b)

            #
            # Logic gates
            #

            elif opcode == BINARY_AND:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.push(a & b)

            elif opcode == BINARY_OR:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.push(a | b)

            elif opcode == BINARY_XOR:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.push(a ^ b)

            elif opcode == BINARY_NOT:
                a = self.stack.pop()
                self.stack.push(~a)

            elif opcode == BINARY_LEFT_SHIFT:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.push(a << b)

            elif opcode == BINARY_RIGHT_SHIFT:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.push(a >> b)

            #
            # Equality
            #

            elif opcode == EQUALS_TO:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.push(a == b)

            elif opcode == NOT_EQUAL_TO:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.push(a != b)

            elif opcode == LESS_THAN:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.push(a < b)

            elif opcode == LESS_EQUAL_THAN:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.push(a <= b)

            elif opcode == GREATER_THAN:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.push(a > b)

            elif opcode == GREATER_EQUAL_THAN:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.push(a >= b)

            #
            # Conditionals
            #

            elif opcode == IF_RUN_NEXT:
                frame.target_IP = self.IP.inst + args[0]
                if not self.stack.pop():
                    self.IP.inst += args[0]

            elif opcode == SKIP_NEXT:
                self.IP.inst += args[0]

            elif opcode == GO_BACK:
                self.IP.inst -= args[0] + 1

            #
            # Uncategorized instructions
            #

            elif opcode == FORWARD_ARGS:
                if frame.stream[self.IP.inst + 1].opcode in ONE_ARG:
                    frame.forwarded_args = [self.stack.pop()]

            elif opcode == ROT_TWO:
                """
                Swaps the positions of the top two stack values.

                PUSH_STACK 1
                PUSH_STACK 2
                ;; stack: 1, 2
                ROT_TWO
                ;; stack: 2, 1
                """
                a = self.stack.pop()
                b = self.stack.pop()
                self.stack.push(a)
                self.stack.push(b)

            elif opcode == ROT_THREE:
                """
                Shifts the third and second stack values up one and
                moves the first one down to the third position.

                PUSH_STACK 1
                PUSH_STACK 2
                PUSH_STACK 3
                ;; stack: 1, 2, 3
                ROT_THREE
                ;; stack: 3, 1, 2
                """
                a = self.stack.pop()
                b = self.stack.pop()
                c = self.stack.pop()
                self.stack.push(a)
                self.stack.push(c)
                self.stack.push(b)

            #
            # Importing
            #

            elif opcode == IMPORT_MODULE:
                """
                Imports a module. Uses string in stack as filename
                and argument as frame number.

                PUSH_STRING_STACK "module.bin\0"
                IMPORT_MODULE 1
                """
                if self.flags.step:
                    print("Importing module")
                module_path = os.path.join(
                    os.getcwd(), os.path.dirname(frame.file), str(self.stack.pop())
                )

                # Check if file exists
                if not os.path.isfile(module_path):
                    logging.error(f"ImportError: '{module_path}' is not a file")

                # Import module
                with open(module_path, "r", encoding="latin1") as file:
                    module_code = parser.parse(file.read())

                # Create a new frame
                if args[0] >= len(self.frames):
                    self.frames.extend([None] * (args[0] - len(self.frames) + 1))

                frame = Frame(module_path)

                # Run the code to initialize the memory
                vm = VirtualMachine("", self.flags)
                vm.main_loop(module_code)
                frame.stream = vm.frames[0].stream
                frame.stream_size = vm.frames[0].stream_size
                frame.memory = vm.frames[0].memory

                self.frames[args[0]] = frame

                self.initialize_markers(args[0])

                if self.flags.step:
                    print("Finished importing\n\nCont. IMPORT_MODULE")

            elif opcode == PUSH_STACK_MODULE:
                """
                Pushes a value from memory in a module to stack.
                """
                self.stack.push(self.frames[args[0]].memory[args[1]])

            elif opcode == GOTO_MODULE:
                """
                Goes to a marker in a module.
                """
                self.last_goto.frame = self.IP.frame
                self.last_goto.inst = self.IP.inst

                target_marker = self.frames[args[0]].memory[args[1]]
                self.IP.frame = args[0]
                self.IP.inst = target_marker.inst

            else:
                logging.error(
                    "Unknown instruction: {}".format(bin(opcode)[2:].rjust(2, "0"))
                )

            if self.flags.step:
                input(
                    "Mem: {}\nStk: {}".format(
                        frame.memory.memory,
                        self.stack.stack,
                    )
                )

    def initialize_markers(self, frame_index: int) -> None:
        """
        Scan the instructions in a stream and perform the following tasks:
        1. Initialize markers into memory
        2. Load modules
        """
        start_frame = self.IP.frame
        start_inst = self.IP.inst

        self.IP.frame = frame_index
        frame = self.frames[frame_index]

        while True:
            inst = self.next_instruction()
            if inst is None:
                break

            if inst.opcode == MAKE_MARKER:
                addr = inst.opargs[0]
                # Only initialize the first occurance of a marker
                if addr < frame.memory.size and isinstance(frame.memory[addr], Marker):
                    continue
                frame.memory[addr] = Marker(self.IP)

            # elif inst.opcode == IMPORT_MODULE:

        self.IP.frame = start_frame
        self.IP.inst = start_inst


class Frame:
    def __init__(self, file: str):
        self.file: str = file

        self.memory: Memory = Memory()

        self.stream: List[Instruction] = []
        self.stream_size: int = 0

        self.forwarded_args: List[Any] = []

        self.target_IP: int = -1
