from typing import Any, List


class Stack:
    def __init__(self) -> None:
        self.stack: List[Any] = []

    def is_empty(self) -> bool:
        return len(self.stack) == 0

    def push(self, value: Any) -> None:
        self.stack.append(value)
        # print(self.stack)

    def pop(self) -> Any:
        if self.is_empty():
            raise Exception("Stack is empty")
        return self.stack.pop()
