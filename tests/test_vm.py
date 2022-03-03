"""
Test features in binarypp.vm.stack
"""

from argparse import Namespace

from binarypp.types import Instruction, Marker
from binarypp.vm import VirtualMachine
from binarypp.vm.opcodes import *


class TestVM:
    def setup_class(self):
        self.vm = VirtualMachine("test_file.bin", Namespace(step=None))
        self.vm.frames[0].stream = [
            Instruction(GOTO_MARKER, [1]),
            Instruction(MAKE_MARKER, [1]),
            Instruction(PUSH_STACK, [48]),
            Instruction(WRITE_TO, [0]),
        ]
        self.vm.frames[0].stream_size = len(self.vm.frames[0].stream) - 1

    def test_setup(self):
        assert self.vm.frames[0].file == "test_file.bin"

    def test_initialize_markers(self):
        self.vm.initialize_markers(0)
        assert isinstance(self.vm.frames[0].memory[1], Marker)
        assert self.vm.frames[0].memory[1].frame == 0
        assert self.vm.frames[0].memory[1].inst == 1

    def test_next_instruction(self):
        inst = self.vm.next_instruction()
        assert inst.opcode == GOTO_MARKER
        assert inst.opargs == [1]
        assert self.vm.IP.frame == 0
        assert self.vm.IP.inst == 0

        # Reset the instruction pointer
        self.vm.IP.inst = -1

    def test_main_loop(self):
        self.vm = VirtualMachine("test_file.bin", Namespace(step=None))
        # TODO: test ALL instructions
        self.vm.main_loop(
            [
                Instruction(PUSH_STACK, [10]),
                Instruction(DUP_TOP, []),
                Instruction(BINARY_MULTIPLY, []),
                Instruction(PUSH_STACK, [1]),
                Instruction(BINARY_ADD, []),
                Instruction(DUP_TOP, []),
                Instruction(PUSH_STACK, [14]),
                Instruction(BINARY_ADD, []),
                Instruction(DUP_TOP, []),
                Instruction(PUSH_STACK, [1]),
                Instruction(BINARY_ADD, []),
                Instruction(DUP_TOP, []),
            ]
        )

        assert self.vm.stack.stack == [101, 115, 116, 116]
        assert self.vm.frames[0].memory.memory == [0]


# class oldTestVM:
#     def setup_class(self):
#         self.vm = VirtualMachine("test_file.bin", Namespace(step=None))
#         self.vm.frames[0].stream = [
#             Instruction(GOTO_MARKER, [1]),
#             Instruction(MAKE_MARKER, [1]),
#             Instruction(PUSH_STACK, [48]),
#             Instruction(WRITE_TO, [0]),
#         ]
#         self.vm.frames[0].stream_size = len(self.vm.frames[0].stream) - 1

#     def test_setup(self):
#         assert self.vm.frames[0].file == "test_file.bin"

#     def test_next_instruction(self):
#         inst = self.vm.next_instruction()
#         assert inst.opcode == GOTO_MARKER
#         assert inst.opargs == [1]
#         assert self.vm.IP.frame == 0
#         assert self.vm.IP.inst == 0

#         # Reset instruction pointer after testing
#         self.vm.IP.inst = -1

#     def test_initialize_markers(self):
#         self.vm.initialize_markers(0)
#         assert self.vm.frames[0].memory[1].index == 1

#     def test_main_loop(self):
#         self.vm.main_loop(
#             [
#                 Instruction(PUSH_STACK, [52]),
#                 Instruction(PUSH_STACK, [2]),
#                 Instruction(BINARY_MULTIPLY,[]),
#                 Instruction(DUP_TOP, []),
#                 Instruction(PUSH_STACK, [1]),
#                 Instruction(BINARY_ADD, []),
#                 Instruction(ROT_TWO, []),
#                 Instruction(STORE_MEMORY, [0]),
#                 Instruction(STORE_MEMORY, [1]),
#                 Instruction(PUSH_STACK, [10]),
#                 Instruction(STORE_MEMORY, [2]),
#             ]
#         )
#         assert self.vm.frames[0].memory.memory == [104, 105, 10]

#         self.vm.main_loop(
#             [
#                 Instruction(PUSH_STACK, [1]),
#                 Instruction(PUSH_STACK, [2]),
#                 Instruction(PUSH_STACK, [3]),
#                 Instruction(ROT_THREE, [])
#             ]
#         )
#         assert self.vm.stack.stack == [3, 1, 2]
