from typing import List, Optional
import binarypp.utils as utils
from binarypp.types import Instruction
from binarypp.vm.opcodes import *
import sys

NO_ARG = (
    POP_STACK,
    DUP_TOP,
    BINARY_ADD,
    BINARY_SUBTRACT,
    BINARY_MULTIPLY,
    BINARY_POWER,
    BINARY_TRUE_DIVIDE,
    BINARY_FLOOR_DIVIDE,
    BINARY_MODULO,
    BINARY_AND,
    BINARY_OR,
    BINARY_XOR,
    BINARY_NOT,
    BINARY_LEFT_SHIFT,
    BINARY_RIGHT_SHIFT,
    EQUAL_TO,
    NOT_EQUAL_TO,
    LESS_THAN,
    LESS_EQUAL_THAN,
    GREATER_THAN,
    GREATER_EQUAL_THAN,
)
ONE_ARG = (
    PUSH_STACK,
    LOAD_MEMORY,
    STORE_MEMORY,
    READ_FROM,
    READ_CHAR_FROM,
    WRITE_TO,
    OPEN_FILE,
    MAKE_MARKER,
    GOTO_MARKER,
    IF_RUN_NEXT,
    SKIP_NEXT,
)
MULTI_ARG = (PUSH_STRING_STACK, PUSH_LONG_STACK)


def parse(code: List[int]) -> List[Instruction]:
    tokens: List[Instruction] = []
    IP = 0

    try:
        while IP < len(code):
            opcode = code[IP]

            if opcode in NO_ARG:
                tokens.append(Instruction(opcode))
            elif opcode in ONE_ARG:
                tokens.append(Instruction(opcode, [code[IP + 1]]))
                IP += 1
            elif opcode in MULTI_ARG:
                if 0 not in code[IP:]:
                    print("Missing a null-terminator at instruction", len(tokens))
                    sys.exit(1)

                args = []
                while code[IP] != 0:
                    IP += 1
                    args.append(code[IP])
                tokens.append(Instruction(opcode, args))
            else:
                print("Unknown opcode: ", utils.to_binary_str(opcode))

            IP += 1
    except IndexError:
        print("An instruction is missing an argument.")
        sys.exit(1)

    return tokens
