import sys


def log_level_zero(log_message: str, log_level: int) -> None:
    pass


def log_level_one(log_message: str, log_level: int) -> None:
    if log_level:
        print(log_message)


def log_level_two(log_message: str, log_level: int) -> None:
    if log_level >= 2:
        print(log_message)


def log_level_three(log_message: str, log_level: int) -> None:
    if log_level >= 3:
        print(log_message)


def error(log_message: str, terminate: bool = True) -> None:
    print("[-]", log_message)
    if terminate:
        sys.exit(1)


def success(log_message: str) -> None:
    print("[+]", log_message)


LOGGING_LEVELS = (log_level_zero, log_level_one, log_level_two, log_level_three)
