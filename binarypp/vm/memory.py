from typing import Any, List


class Memory:
    def __init__(self):
        self.memory: List[Any] = [0]
        self.mem_size: int = 1

    def __setitem__(self, index: int, value: Any) -> None:
        if index >= self.mem_size:
            # print("Expanding memory")
            amount = index - self.mem_size + 1
            self.memory.extend([0] * amount)
            self.mem_size += amount
        # print("Writing '{}' to MEMORY[{}]".format(value, index))
        self.memory[index] = value

    def __getitem__(self, index: int) -> Any:
        if index == 0:
            raise Exception("Accessing reserved memory: MEMORY[0]")
        # print("Accessing MEMORY[{}]".format(index))
        return self.memory[index]
