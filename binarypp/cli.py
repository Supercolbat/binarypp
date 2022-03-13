import argparse
import os
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
        "-V",
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
        if args.compile:
            logging.error("No output file was supplied :(")
        else:
            logging.error("No file was supplied :(")

    # Check if file does not exist
    target_file = args.compile if args.compile else args.FILE
    if not os.path.isfile(target_file):
        # Suggest possible file in case of typo
        # TODO: Current method is less than optimal
        files = []
        dir_path = os.path.dirname(target_file)
        dir_path = dir_path if dir_path else "."

        for (dirpath, dirnames, filenames) in os.walk(dir_path):
            files.extend(filenames)
            break

        match = utils.fuzzy_search(os.path.basename(target_file), files)

        if match is not None:
            logging.error(
                "'{}' does not exist! Did you mean '{}'? (yN)".format(
                    target_file,
                    f"{dir_path}/{match}",
                ),
                False,
                True,
            )

            if input().lower()[0] != "y":
                sys.exit(0)

            if args.compile:
                args.compile = f"{dir_path}/{match}"
            else:
                args.FILE = f"{dir_path}/{match}"
        else:
            logging.error("'{}' does not exist! Are you in the right directory?")

    if args.compile:
        with open(args.compile, "r", encoding="utf-8") as file:
            code = file.read()

        # Check for missing args
        binarypp.parser.parse(code)

        # Strip away the interpret flag if present
        if code.startswith("00000000"):
            code = code[8:]

        compiled_code = utils.binary_to_chars(
            list(filter(utils.is_binary, code.split()))
        )

        try:
            with open(args.FILE, "w+", encoding="latin1") as file:
                file.write(compiled_code)

            logging.success("Successfully compiled the program")
        except PermissionError:
            logging.error(
                "Could not write to file. You might need to make it writable"
                "by running 'chmod +w {}'".format(args.FILE)
            )

    else:
        with open(args.FILE, "r", encoding="latin1") as file:
            code = file.read()

        vm = VirtualMachine(args.FILE, args)
        vm.main_loop(binarypp.parser.parse(code))
