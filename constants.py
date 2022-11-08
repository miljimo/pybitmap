import os
from pathlib import Path

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def join(*args) -> str:
    result = ""
    for path in args:
        result = os.path.join(result, os.path.realpath(path))
    return result


if __name__ == "__main__":
    print(ROOT_DIR)
