from typing import List, Union

import binarypp.utils as utils


class String:
    def __init__(self, data: Union[List[int], str, int]):
        self.data: List[int] = []

        if isinstance(data, str):
            self.data = [ord(element) for element in data]
        elif isinstance(data, list):
            self.data = data
        else:
            self.data = [data]

    def __repr__(self) -> str:
        return "".join(chr(code) for code in self.data)


class Instruction:
    def __init__(self, opcode: int, opargs: List[int] = []):
        self.opcode: int = opcode
        self.opargs: List[int] = opargs

    def __repr__(self) -> str:
        return "Instruction({}, [{}])".format(
            utils.to_binary_str(self.opcode),
            ", ".join([utils.to_binary_str(code) for code in self.opargs]),
        )


class Pointer:
    def __init__(self, frame: int, inst: int):
        self.frame = frame
        self.inst = inst


class Marker(Pointer):
    def __init__(self, pointer: Pointer):
        super().__init__(pointer.frame, pointer.inst)

    def __repr__(self) -> str:
        return "Marker({}, {})".format(self.frame, self.inst)
