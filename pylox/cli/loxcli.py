"""loxcli

Module for pylox command line interface (cli)
"""

from dataclasses import dataclass
import argparse
from pathlib import Path
import logging

def toggle_debug(debug_on: bool):
    """Toggles the verbosity of the interpreter logs"""
    for logger in logging.root.manager.loggerDict.values():
        if isinstance(logger, logging.PlaceHolder):
            continue
        if debug_on:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.ERROR)

@dataclass
class Args:
    src: Path | None
    debug_on: bool
    rpolish: bool

def get_args() -> Args:
    """Handles the various cli arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--src", help="path to source file", type=Path, default=None)
    parser.add_argument("--debug", help="switch to debug mode", action="store_true", default=False)
    parser.add_argument("--rpolish", help="ast prints using Reverse Polish Notation", action="store_true", default=False)
    args = parser.parse_args()
    return Args(args.debug, args.src, args.rpolish)
