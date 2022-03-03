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
                        f"You are missing a 00000000 to end instruction #{len(tokens)}"
                    )

                # Read all arguments until 00000000 is reached
                args = []
                IP += 1
                while code[IP] != 0:
                    args.append(code[IP])
                    IP += 1

                tokens.append(Instruction(opcode, args))

            else:
                # This formatting may not work on all terminals
                logging.error(
                    f"Uh oh! This instruction isn't defined! "
                    f"{utils.to_binary_str(opcode)}\n"
                    f"   Check instruction #{len(tokens)}"
                )

            IP += 1

    except IndexError:
        logging.error(
            "We don't know where, but one of your instructions is missing an argument!"
        )

    return tokens
