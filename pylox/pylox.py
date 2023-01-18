"""pylox.py

Main module for running the application
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

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--src", help="path to source file", type=Path)
    parser.add_argument("--verbose", help="increase output verbosity", action="store_true")
    args = parser.parse_args()

    lox = Lox()

    pylox_info = ProgramInfo(
        name="Pylox",
        version="0.1.0",
        docs_url="https://craftinginterpreters.com/"
    )
    
    is_verbose: bool = args.verbose
    if is_verbose:
        toggle_verbose(True)
    else:
        toggle_verbose(False)

    src: Path = args.src
    if src and src.exists():
        lox.run_file(args)
    else:
        pylox_info.print()
        lox.run_prompt()
