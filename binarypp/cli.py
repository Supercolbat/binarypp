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

    with open(file, "rb") as f:
        code = f.read()

    if "-t" in sys.argv:
        with open("code.bin", "wb+") as f:
            f.write(bytes("".join([chr(int(c, 2)) for c in code.split()]), "utf-8"))
        return
    
    vm = VirtualMachine()
    vm.main_loop(code)
    