from typing import List

import binarypp.logging as logging
import binarypp.utils as utils
from binarypp.types import Instruction
from binarypp.vm.opcodes import *


def parse(raw_code: str) -> List[Instruction]:
    tokens: List[Instruction] = []
    IP = 0

    # Check if file is in interpret-mode
    code_split = raw_code.split()
    if code_split[0] == "00000000":
        code = [int(c, 2) for c in list(filter(utils.is_binary, code_split))]
        code.pop(0)
    else:
        code = [ord(c) for c in raw_code]

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

            elif opcode in TWO_ARG:
                if IP > 0 and code[IP - 1] == FORWARD_ARGS:
                    tokens.append(Instruction(opcode))
                else:
                    tokens.append(Instruction(opcode, [code[IP + 1], code[IP + 2]]))
                    IP += 2

            elif opcode in MULTI_ARG:
                if 0 not in code[IP:]:
                    logging.error(
                        f"Missing a null-terminator at instruction {len(tokens)}"
                    )

                # Read all arguments until 00000000 is reached
                args = []
                while code[IP + 1] != 0:
                    IP += 1
                    args.append(code[IP])

                # Skip the 00000000 byte
                IP += 1
                tokens.append(Instruction(opcode, args))

            else:
                logging.error("Unknown opcode: " + utils.to_binary_str(opcode))

            IP += 1

    except IndexError:
        logging.error("An instruction is missing an argument.")

    return tokens
