from typing import List, Optional

# ================ #
# Binary functions #
# ================ #


def is_binary(code: str) -> bool:
    return code.count("0") + code.count("1") == len(code) == 8


def to_binary_str(num: int) -> str:
    return bin(num)[2:].rjust(8, "0")


def binary_to_chars(binary: List[str]) -> str:
    return "".join([chr(int(code, 2)) for code in binary])


# ==================== #
# Levenshtein Distance #
# ==================== #


def levenshtein_distance(sample: str, test: str) -> int:
    # Sources:
    # https://stackabuse.com/levenshtein-distance-and-text-similarity-in-python/
    # https://www.datacamp.com/community/tutorials/fuzzy-string-python

    sample, test = sample.lower(), test.lower()
    rows = len(sample) + 1
    cols = len(test) + 1
    matrix = [[0] * cols for _ in range(rows)]

    # Populate the matrix
    for x in range(1, rows):
        for y in range(1, cols):
            matrix[x][0] = x
            matrix[0][y] = y

    # Calculate the cost
    for x in range(1, rows):
        for y in range(1, cols):
            if sample[x - 1] == test[y - 1]:
                matrix[x][y] = min(
                    matrix[x - 1][y] + 1, matrix[x - 1][y - 1], matrix[x][y - 1] + 1
                )
            else:
                matrix[x][y] = min(
                    matrix[x - 1][y] + 1, matrix[x - 1][y - 1] + 1, matrix[x][y - 1] + 1
                )

    return matrix[rows - 1][cols - 1]


def fuzzy_search(query: str, tests: List[str]) -> Optional[str]:
    distances = [(test, levenshtein_distance(query, test)) for test in tests]
    distances.sort(key=lambda match: match[1])

    if distances:
        return min(
            filter(lambda match: match[1] & distances[0][1], distances),
            key=lambda m: m[1],
        )[0]
    else:
        return None
