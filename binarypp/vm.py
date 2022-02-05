from typing import Any, List, Union
from sys import stdout, stdin
import os.path
import io
from binarypp.stack import Stack
from binarypp.memory import Memory
from binarypp.types import Marker
from binarypp.opcodes import *

# fmt: off
MODES = ["r", "r+", "rb", "rb+", # 0000 - 0011
         "w", "w+", "wb", "wb+", # 0100 - 0111
         "a", "a+", "ab", "ab+", # 1000 - 1011
         "x", "x+", "xb", "xb+"] # 1100 - 1111
# fmt: on


class VirtualMachine:
    def __init__(self):
        self.stack = Stack()
        self.memory = Memory()

        self.IP: int = -1  # Instruction Pointer
        self.stream: List[int] = []
        self.stream_size: int = 0

    def next_instruction(self) -> Union[int, None]:
        if self.IP < self.stream_size:
            self.IP += 1
            return self.stream[self.IP]

    def main_loop(self, stream: List[int]) -> None:
        self.stream = stream
        self.stream_size = len(stream) - 1

        while (opcode := self.next_instruction()) != None:
            # print(bin(opcode)[2:].rjust(8, "0"))
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
                self.stack.push(self.next_instruction())

            elif opcode == PUSH_STRING_STACK:
                """
                Pushes all codes as a string until a null-terminator is reached.

                PUSH_STRING_STACK Hello\0
                PUSH_STRING_STACK  world\0
                """
                string = ""
                while (oparg := self.next_instruction()) != 0:
                    # print(chr(oparg), end="")
                    string += chr(oparg)
                # print()
                self.stack.push(string)

            elif opcode == PUSH_LONG_STACK:
                """
                Pushes all codes as an int until a null-terminator is reached.

                PUSH_LONG_STACK 255 255 10\0
                """
                long = 0
                while (oparg := self.next_instruction()) != 0:
                    # print(oparg, end=" ")
                    long += oparg
                # print()g
                self.stack.push(long)

            elif opcode == STORE_MEMORY:
                """
                Stores the top-most value in stack to the memory address.
                0 is a reserved address.

                PUSH_STACK 5
                STORE_MEMORY 1
                """
                addr = self.next_instruction()
                if addr == 0:
                    raise Exception("Accessing reserved memory")
                self.memory[addr] = self.stack.pop()

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
                addr = self.next_instruction()

                if addr == 0:
                    self.stack.push(stdin.read())
                else:
                    stream = self.memory[addr]
                    if not isinstance(stream, io.TextIOWrapper):
                        raise Exception("MEMORY[{}] is not a file".format(addr))

                    terminator = chr(self.stack.pop())
                    string = ""
                    while (char := stream.read(1)) != terminator and char != "":
                        string += char
                    self.stack.push(string)

            elif opcode == WRITE_TO:
                """
                Writes the top-most stack to a source.
                0 is stdout. Any other value is reads from memory to determine source.
                """
                addr = self.next_instruction()
                if addr == 0:
                    content = self.stack.pop()
                    if isinstance(content, int):
                        stdout.write(chr(content))
                    else:
                        stdout.write(content)
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
                mode = self.next_instruction()
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
                self.memory[self.next_instruction()] = Marker(self.IP)

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
                addr = self.next_instruction()
                target_marker = self.memory[addr]
                if not isinstance(target_marker, Marker):
                    raise Exception("Invalid marker at MEMORY[{}]".format(addr))
                self.IP = target_marker.index - 1

            #
            # Mathematics
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

            else:
                raise NotImplemented(
                    "Unknown instruction: {}".format(bin(opcode)[2:].rshift(2, "0"))
                )
