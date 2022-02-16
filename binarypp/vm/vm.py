from typing import Any, List, Union
from sys import stdout, stdin
import os.path
import io
from argparse import Namespace
import binarypp.parser as parser
import binarypp.utils as utils
from binarypp.types import Marker, String, Instruction
from binarypp.vm.stack import Stack
from binarypp.vm.memory import Memory
from binarypp.vm.opcodes import *
from binarypp.vm.opmap import OP_MAP

# fmt: off
MODES = ["r", "r+", "rb", "rb+", # 0000 - 0011
         "w", "w+", "wb", "wb+", # 0100 - 0111
         "a", "a+", "ab", "ab+", # 1000 - 1011
         "x", "x+", "xb", "xb+"] # 1100 - 1111
# fmt: on


class VirtualMachine:
    def __init__(self, flags: List[Namespace]):
        self.flags: List[Namespace] = flags
        
        self.stack = Stack()
        self.memory = Memory()

        self.IP: int = -1  # Instruction Pointer
        self.stream: List[Instruction] = []
        self.stream_size: int = 0

        self.last_goto: int = 0
        self.forwarded_args: List[Any] = []

    def next_instruction(self) -> Union[int, None]:
        if self.IP < self.stream_size:
            self.IP += 1
            return self.stream[self.IP]

    def main_loop(self, stream: List[int]) -> None:
        self.stream = parser.parse(stream)
        self.stream_size = len(self.stream) - 1

        self.initialize_markers()

        while (inst := self.next_instruction()) != None:
            opcode = inst.code
            if self.forwarded_args:
                args = self.forwarded_args
                self.forwarded_args = []
            else:
                args = inst.arguments

            # print(utils.to_binary_str(opcode), args)

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
                self.stack.push(self.memory[args[0]])

            elif opcode == STORE_MEMORY:
                """
                Stores the top-most value in stack to the memory address.
                0 is a reserved address.

                PUSH_STACK 5
                STORE_MEMORY 1
                """
                self.memory[args[0]] = self.stack.pop()

            elif opcode == DUP_TOP:
                """
                Duplicates the top-most stack value.

                PUSH_STACK 5
                DUP_TOP
                """
                val = self.stack.pop()
                self.stack.push(val)
                self.stack.push(val)

            elif opcode == READ_FROM:
                """
                Reads values from a source until the terminator is reached (top stack). Pushes text to stack. Terminator is consumed but excluded.
                0 is stdin. Any other value is read from memory to determine source.

                READ_FROM 0 (stdin)
                PUSH_STRING_STACK "file.txt"
                OPEN_FILE 0
                STORE_MEMORY 1
                PUSH_STACK \32
                READ_FROM 1
                WRITE_TO 0 (stdin)
                """
                addr = args[0]

                if addr == 0:
                    self.stack.push(String(stdin.read()))
                else:
                    stream = self.memory[addr]
                    if not isinstance(stream, io.TextIOWrapper):
                        raise Exception("MEMORY[{}] is not a file".format(addr))

                    terminator = chr(self.stack.pop())
                    string = ""
                    while (char := stream.read(1)) != terminator and char != "":
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
                    stream = self.memory[addr]
                    if not isinstance(stream, io.TextIOWrapper):
                        raise Exception("MEMORY[{}] is not a file".format(addr))

                    self.stack.push(String(stream.read(1)))

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
                    stream = self.memory[addr]
                    if not isinstance(stream, io.TextIOWrapper):
                        raise Exception("MEMORY[{}] is not a file".format(addr))

                    stream.write(self.stack.pop())
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
                    raise Exception(
                        "Invalid file mode {}. Range: 0b0000-0b1111.".format(bin(mode))
                    )

            elif opcode == MAKE_MARKER:
                """
                Creates a marker at its current position in the code. Stores the marker at the given position in memory.

                MAKE_MARKER 1
                """
                self.memory[args[0]] = Marker(self.IP)

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
                    self.IP = self.last_goto
                    continue

                target_marker = self.memory[args[0]]
                if not isinstance(target_marker, Marker):
                    raise Exception("Invalid marker at MEMORY[{}]".format(args[0]))

                self.last_goto = self.IP
                self.IP = target_marker.index

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
                if not self.stack.pop():
                    self.IP += args[0]

            elif opcode == SKIP_NEXT:
                # the oparg should point to the last instruction to be skipped
                # next main_loop iteration should increment self.IP by one to the next instruction
                # adding one here is a temporary fix until further investigation takes place
                # EDIT: possibly fixed
                self.IP += args[0]

            #
            # Uncategorized instructions
            #

            elif opcode == FORWARD_ARGS:
                if self.stream[self.IP + 1].code in ONE_ARG:
                    self.forwarded_args = [self.stack.pop()]

            elif opcode == ROT_TWO:
                a = self.stack.pop()
                b = self.stack.pop()
                self.stack.push(a)
                self.stack.push(b)

            else:
                raise NotImplementedError(
                    "Unknown instruction: {}".format(bin(opcode)[2:].rjust(2, "0"))
                )

            if self.flags.step:
                input("\nInst: {} {} ({})\nMem: {}\nStk: {}".format(OP_MAP[opcode], args, self.forwarded_args, self.memory.memory, self.stack.stack))

    def initialize_markers(self):
        while (inst := self.next_instruction()) != None:
            if inst.code == MAKE_MARKER:
                addr = inst.arguments[0]
                # Only initialize the first occurance of a marker
                if addr < self.memory.size and isinstance(self.memory[addr], Marker):
                    continue
                self.memory[addr] = Marker(self.IP)

        self.IP = -1
