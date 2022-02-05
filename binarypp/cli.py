import sys
import os.path
from binarypp.vm import VirtualMachine


def main():
    if len(sys.argv) == 1:
        print("No file supplied")
        sys.exit(1)

    file = sys.argv[-1]

    if not os.path.isfile(file):
        print("{} is not a file".format(file))
        sys.exit(1)

    if "-t" in sys.argv:
        with open(file, "r") as f:
            code = [int(c, 2) for c in f.read().split()]
        with open("code.bin", "w+") as f:
            f.write("".join([chr(c) for c in code]))
    else:
        with open(file, "r") as f:
            code = [ord(inst) for inst in f.read()]

        vm = VirtualMachine()
        vm.main_loop(code)
