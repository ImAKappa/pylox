"""lox.cli

Module for pylox command line interface (cli)
"""

from dataclasses import dataclass
import argparse
from pathlib import Path
import logging

def toggle_verbose(is_verbose: bool):
    """Toggles the verbosity of the interpreter logs"""
    for logger in logging.root.manager.loggerDict.values():
        if isinstance(logger, logging.PlaceHolder):
            continue
        if is_verbose:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.ERROR)

@dataclass
class Args:
    is_verbose: bool
    src: Path | None
    rpolish: bool

def get_args() -> Args:
    """Handles the various cli arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--src", help="path to source file", type=Path)
    parser.add_argument("--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("--rpolish", help="ast prints using Reverse Polish Notation", action="store_true")
    args = parser.parse_args()
    return Args(args.verbose, args.src, args.rpolish)
