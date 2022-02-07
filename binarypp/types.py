from typing import List, Optional, Union
import binarypp.utils as utils


class Marker:
    def __init__(self, index: int):
        self.index = index

    def __repr__(self):
        return "Marker({})".format(self.index)


class String:
    def __init__(self, data: Union[List[int], str, int]):
        self.data: List[int] = []

        if isinstance(data, str):
            self.data = [ord(element) for element in data]
        elif isinstance(data, list):
            self.data = data
        else:
            self.data = [data]

    def __repr__(self):
        return "".join(chr(code) for code in self.data)

    def __str__(self):
        return "".join(chr(code) for code in self.data)


class Instruction:
    def __init__(self, code: int, arguments: Optional[List[int]] = []):
        self.code = code
        self.arguments = arguments

    def __repr__(self):
        return "Instruction({}, {})".format(
            utils.to_binary_str(self.code), self.arguments
        )
