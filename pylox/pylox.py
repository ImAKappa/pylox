"""pylox

This module provides the main entry point to the logic of the interpreter
"""

import sys
from rich.console import Console
from pylox.cli.loxcli import Args
import pylox.cli.loxcli as loxcli
from pylox.cli import programinfo
from pylox.engine.lox import Lox

def run(args: Args) -> None:
    """Runs the Pylox interpreter, given some arguments"""
    lox = Lox()
    loxcli.toggle_debug(args.debug)

    if args.rpolish:
        lox.astprinter.rev_polish_notation = True

    if args.src:
        if args.src.exists():
            lox.run_file(args.src)
        else:
            # TODO: Output to stderror
            stderr = Console(stderr=True)
            stderr.print(f"[Error] Could not find file: '{args.src}'")
    else:
        pylox_info = programinfo.ProgramInfo(
            name="Lox",
            version="0.1.0",
            docs_url="https://craftinginterpreters.com/"
        )
        # TODO: Create a __str__ method on ProgramInfo instead of a `print` method
        pylox_info.print()
        lox.run_prompt()