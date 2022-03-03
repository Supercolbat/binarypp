import binarypp.parser as parser
from binarypp.vm.opcodes import *


def test_parser():
    raw_code = """
00000000
00000100 00110000
00001010 00000000"""
    insts = parser.parse(raw_code)

    assert insts[0].opcode == PUSH_STACK
    assert insts[0].opargs == [48]
    assert insts[1].opcode == WRITE_TO
    assert insts[1].opargs == [0]

    raw_code = "\x04\x30\x0a\x00"
    insts = parser.parse(raw_code)

    assert insts[0].opcode == PUSH_STACK
    assert insts[0].opargs == [48]
    assert insts[1].opcode == WRITE_TO
    assert insts[1].opargs == [0]
