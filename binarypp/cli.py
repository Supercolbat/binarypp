import sys
import os.path
import argparse
import binarypp
import binarypp.parser
import binarypp.utils as utils
from binarypp.vm import VirtualMachine


def main():
    parser = argparse.ArgumentParser(binarypp.__name__)
    parser.add_argument(
        "--translate",
        "-t",
        help="Translate the target file and write to supplied path.",
    )
    parser.add_argument(
        "--verbosity",
        "-v",
        help="Change verbosity level.",
        action="store_true",
    )
    parser.add_argument(
        "--version",
        help="Prints the version and exits.",
        action="store_true",
    )
    parser.add_argument("FILE", help="Target file.", nargs="?")
    args = parser.parse_args()

    if args.version:
        print("Binary++", binarypp.__version__)
        sys.exit(0)
    
    if not args.FILE:
        print("Missing FILE argument")
        sys.exit(1)

    if not os.path.isfile(args.FILE):
        print("{} is not a file".format(args.FILE))
        sys.exit(1)

    if args.translate:
        with open(args.translate, "r") as file:
            code = file.read()
        code = utils.binary_to_chars(list(filter(utils.is_binary, code.split())))

        # Check for missing args
        binarypp.parser.parse([ord(char) for char in code])

        with open(args.FILE, "w+") as file:
            file.write(code)

        print("Sucessfully translated file")
    else:
        with open(args.FILE, "r") as file:
            code = utils.chars_to_binary(file.read())

        vm = VirtualMachine()
        vm.main_loop(code)
        # print(vm.memory.memory)
