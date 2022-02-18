import sys
from typing import List

import binarypp.utils as utils
from binarypp.types import Instruction
from binarypp.vm.opcodes import *


def parse(code: List[int]) -> List[Instruction]:
    tokens: List[Instruction] = []
    IP = 0

    try:
        while IP < len(code):
            opcode = code[IP]
            # print(utils.to_binary_str(opcode))

            if opcode in NO_ARG:
                tokens.append(Instruction(opcode))

            elif opcode in ONE_ARG:
                if IP > 0 and code[IP - 1] == FORWARD_ARGS:
                    tokens.append(Instruction(opcode))
                else:
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
                raise NameError("Unknown opcode: " + utils.to_binary_str(opcode))

            IP += 1

    except IndexError:
        print("An instruction is missing an argument.")
        sys.exit(1)

    return tokens
