import sys
import os.path
import argparse
import binarypp
import binarypp.parser
import binarypp.utils as utils
from binarypp.vm import VirtualMachine


def main() -> None:
    parser = argparse.ArgumentParser(binarypp.__name__)
    parser.add_argument(
        "--compile",
        "-c",
        help="Compiles the supplied file and writes to the target file.",
    )
    parser.add_argument(
        "--interpret",
        "-i",
        help="Interprets the target file and executes it.",
        action="store_true",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        help="Change verbosity level.",
        action="count",
        default=0,
    )
    parser.add_argument(
        "--step",
        "-s",
        help="Runs the code step by step.",
        action="store_true",
    )
    parser.add_argument(
        "--version",
        help="Prints the version and exits.",
        action="store_true",
    )
    parser.add_argument("FILE", help="Target file.", nargs="?")
    args = parser.parse_args()

    # Version flag takes priority
    if args.version:
        print("Binary++", binarypp.__version__)
        sys.exit(0)

    # Check if file argument is missing
    if not args.FILE:
        print("[-] Missing FILE argument")
        sys.exit(1)

    # Verify file exists
    if not os.path.isfile(args.compile if args.compile else args.FILE):
        print("[-] {} is not a file".format(args.FILE))
        sys.exit(1)

    if args.compile:
        with open(args.compile, "r") as file:
            code = file.read()
        code = utils.binary_to_chars(list(filter(utils.is_binary, code.split())))

        # Check for missing args
        binarypp.parser.parse([ord(char) for char in code])

        with open(args.FILE, "w+") as file:
            file.write(code)

        print("[+] Successfully compiled file")

    elif args.interpret:
        with open(args.FILE, "r") as file:
            code = file.read()

        code = list(filter(utils.is_binary, code.split()))

        # Check for missing args
        binarypp.parser.parse([ord(char) for char in utils.binary_to_chars(code)])

        code = [int(code, 2) for code in code]

        vm = VirtualMachine(args)
        vm.main_loop(code)

    else:
        with open(args.FILE, "r") as file:
            code = utils.chars_to_binary(file.read())

        vm = VirtualMachine(args)
        vm.main_loop(code)
        # print(vm.memory.memory)
