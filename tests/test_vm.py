"""
Test features in binarypp.vm.stack
"""

from argparse import Namespace

from binarypp.types import Instruction
from binarypp.vm import VirtualMachine
from binarypp.vm.opcodes import *


class TestVM:
    def setup_class(self):
        self.vm = VirtualMachine(Namespace(step=None))
        self.vm.stream = [
            Instruction(GOTO_MARKER, [1]),
            Instruction(MAKE_MARKER, [1]),
            Instruction(PUSH_STACK, [48]),
            Instruction(WRITE_TO, [0]),
        ]
        self.vm.stream_size = len(self.vm.stream) - 1

    def test_next_instruction(self):
        inst = self.vm.next_instruction()
        assert inst.opcode == GOTO_MARKER
        assert inst.opargs == [1]
        assert self.vm.IP == 0

        # Reset instruction pointer after testing
        self.vm.IP = -1

    def test_initialize_markers(self):
        self.vm.initialize_markers()
        assert self.vm.memory[1].index == 1

    def test_main_loop(self):
        # Prints out "hi"
        self.vm.main_loop(
            [
                PUSH_STACK,
                52,
                PUSH_STACK,
                2,
                BINARY_MULTIPLY,
                DUP_TOP,
                PUSH_STACK,
                1,
                BINARY_ADD,
                ROT_TWO,
                STORE_MEMORY,
                0,
                STORE_MEMORY,
                1,
                PUSH_STACK,
                10,
                STORE_MEMORY,
                2,
            ]
        )
        assert self.vm.memory.memory == [104, 105, 10]

        self.vm.main_loop(
            [
                PUSH_STACK,
                1,
                PUSH_STACK,
                2,
                PUSH_STACK,
                3,
            ]
        )
        assert self.vm.stack.stack == [1, 2, 3]
