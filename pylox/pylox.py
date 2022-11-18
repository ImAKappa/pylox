import sys
from rich import print as rprint

from lox import Lox

num_args = len(sys.argv)
args = sys.argv

lox = Lox()

if __name__ == "__main__":

    if num_args > 2:
        rprint("Usage: pylox [script]")
        sys.exit(64)
    if num_args == 2:
        lox.run_file(args[1])
    else:
        lox.run_prompt()
