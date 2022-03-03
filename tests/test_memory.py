"""
Test features in binarypp.vm.memory
"""

from binarypp.vm.memory import Memory


class TestMemory:
    def setup_class(self):
        self.memory = Memory()

        assert self.memory.memory == [0]
        assert self.memory.size == 1

    def test___setitem__(self):
        self.memory[2] = "Hello, world!"
        assert len(self.memory.memory) == 3

    def test___getitem__(self):
        assert self.memory[2] == "Hello, world!"
        assert self.memory[5] == 0

    def test__expand_memory_util(self):
        self.memory._expand_memory_until(10)
        assert self.memory.memory == [0, 0, "Hello, world!", 0, 0, 0, 0, 0, 0, 0, 0]
