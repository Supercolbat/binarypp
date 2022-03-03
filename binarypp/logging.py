import os
import sys

#
# Check if the NO_COLOR environment variable is set.
# If it is, provide alternative log messages.
#
if os.getenv("NO_COLOR"):

    def log_level_one(log_message: str, log_level: int) -> None:
        if log_level:
            print("INFO: ", log_message)

    def log_level_two(log_message: str, log_level: int) -> None:
        if log_level >= 2:
            print("INFO: ", log_message)

    def log_level_three(log_message: str, log_level: int) -> None:
        if log_level >= 3:
            print("INFO: ", log_message)

    def error(log_message: str, terminate: bool = True) -> None:
        sys.stderr.write("✗ " + log_message + "\n")
        if terminate:
            sys.exit(1)

    def success(log_message: str) -> None:
        print("✓", log_message)


#
# If the NO_COLOR environment variable is set, then
# provide color in the output.
#
else:

    def log_level_one(log_message: str, log_level: int) -> None:
        if log_level:
            print("\u001b[36mi\u001b[0m", log_message)

    def log_level_two(log_message: str, log_level: int) -> None:
        if log_level >= 2:
            print("\u001b[36mi\u001b[0m", log_message)

    def log_level_three(log_message: str, log_level: int) -> None:
        if log_level >= 3:
            print("\u001b[36mi\u001b[0m", log_message)

    def error(log_message: str, terminate: bool = True) -> None:
        sys.stderr.write("❌ " + log_message + "\n")
        if terminate:
            sys.exit(1)

    def success(log_message: str) -> None:
        print("✅", log_message)


LOGGING_LEVELS = (log_level_one, log_level_two, log_level_three)
