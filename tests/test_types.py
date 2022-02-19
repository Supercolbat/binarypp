"""
Test features in binarypp.types
"""

from binarypp.types import Instruction, Marker, String


def test_marker():
    new_marker = Marker(5)
    assert new_marker.index == 5
    assert repr(new_marker) == "Marker(5)"


def test_string():
    str_string = String("hello")
    list_string = String([104, 101, 108, 108, 111])
    int_string = String(104)

    assert str_string.data == [104, 101, 108, 108, 111]
    assert list_string.data == [104, 101, 108, 108, 111]
    assert int_string.data == [104]

    assert repr(str_string) == "hello"
    assert repr(list_string) == "hello"
    assert repr(int_string) == "h"


def test_instruction():
    new_instruction = Instruction(0b00000100, [0b00001010])

    assert new_instruction.opcode == 0b00000100
    assert new_instruction.opargs == [0b00001010]
    assert repr(new_instruction) == "Instruction(00000100, [00001010])"