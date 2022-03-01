from typing import Any, List

import binarypp.logging as logging

class Memory:
    def __init__(self) -> None:
        self.memory: List[Any] = [0]
        self.size: int = 1

    def __setitem__(self, index: int, value: Any) -> None:
        if index >= self.size:
            self._expand_memory_until(index)

        # print("Writing '{}' to MEMORY[{}]".format(value, index))
        self.memory[index] = value

    def __getitem__(self, index: int) -> Any:
        if index == 0:
            logging.error("Accessing reserved memory: MEMORY[0]")

        if index >= self.size:
            self._expand_memory_until(index)

        # print("Accessing MEMORY[{}]".format(index))
        return self.memory[index]

    def _expand_memory_until(self, index: int) -> None:
        amount = index - self.size + 1
        self.memory.extend([0] * amount)
        # print("Expanding memory by", amount, "cells")
        self.size += amount
