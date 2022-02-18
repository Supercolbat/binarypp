from typing import List


def is_binary(code: str) -> bool:
    return code.count("0") + code.count("1") == len(code) == 8


def to_binary_str(num: int) -> str:
    return bin(num)[2:].rjust(8, "0")


def binary_to_chars(binary: List[str]) -> str:
    return "".join([chr(int(code, 2)) for code in binary])
