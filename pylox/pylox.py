"""pylox.py

Main module for running the pylox application
"""

import sys
import argparse
from pathlib import Path
import logging
from utils.programinfo import ProgramInfo
from lox import Lox

def toggle_verbose(is_verbose: bool):
    for logger in logging.root.manager.loggerDict.values():
        if is_verbose:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.ERROR)

def main(src: Path = None, is_verbose = False):
    lox = Lox()

    pylox_info = ProgramInfo(
        name="Pylox",
        version="0.1.0",
        docs_url="https://craftinginterpreters.com/"
    )

    if is_verbose:
        toggle_verbose(True)
    else:
        toggle_verbose(False)

    if src:
        if not src.exists():
            print("Could not find file")
            sys.exit(64)
        lox.run_file(src)
    else:
        pylox_info.print()
        lox.run_prompt()

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--src", help="path to source file", type=Path)
    parser.add_argument("--verbose", help="increase output verbosity", action="store_true")
    args = parser.parse_args()

    is_verbose: bool = args.verbose
    src: Path = args.src

    main(src=src, is_verbose=is_verbose)