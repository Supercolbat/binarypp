"""
Test features in binarypp.vm.memory
"""

from binarypp.vm.memory import Memory


class TestMemory:
    def setup_class(self):
        self.memory = Memory()

    def test___setitem__(self):
        self.memory[2] = "Hello, world!"
        assert len(self.memory.memory) == 3

    def test___getitem__(self):
        assert self.memory[2] == "Hello, world!"
        assert self.memory[5] == 0
