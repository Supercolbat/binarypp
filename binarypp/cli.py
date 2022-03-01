import argparse
import os.path
import sys

import binarypp
import binarypp.logging as logging
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
        logging.error("Missing FILE argument")

    # Verify file exists
    if not os.path.isfile(args.compile if args.compile else args.FILE):
        logging.error("{} is not a file".format(args.FILE))

    if args.compile:
        with open(args.compile, "r", encoding="utf-8") as file:
            code = file.read()

        # Check for missing args
        binarypp.parser.parse(code)

        compiled_code = utils.binary_to_chars(
            list(filter(utils.is_binary, code.split()))
        )

        with open(args.FILE, "w+", encoding="latin1") as file:
            file.write(compiled_code)

        logging.success("Successfully compiled file")

    else:
        with open(args.FILE, "r", encoding="latin1") as file:
            code = file.read()

        vm = VirtualMachine(args.FILE, args)
        vm.main_loop(binarypp.parser.parse(code))
