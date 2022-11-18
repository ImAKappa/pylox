import sys

from utils.programinfo import ProgramInfo
from lox import Lox

num_args = len(sys.argv)
args = sys.argv

lox = Lox()

pylox_info = ProgramInfo(
    name="Pylox",
    version="0.1.0",
    docs_url="https://craftinginterpreters.com/"
)

if __name__ == "__main__":

    if num_args > 2:
        print("Usage: pylox [script]")
        sys.exit(64)
    if num_args == 2:
        lox.run_file(args[1])
    else:
        pylox_info.print()
        lox.run_prompt()
