"""
Test features in binarypp.vm.stack
"""

from binarypp.vm.stack import Stack


class TestStack:
    def setup_class(self):
        self.stack = Stack()

    def test_is_empty(self):
        assert self.stack.is_empty()

    def test_push(self):
        self.stack.push(1)
        assert self.stack.stack == [1]

    def test_pop(self):
        assert self.stack.pop() == 1
