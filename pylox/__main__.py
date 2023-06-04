"""pylox.py

Main module for running the pylox application
"""

import sys
import pylox.cli as loxcli
from pylox.cli import programinfo
from pylox.engine.lox import Lox

def main():
    lox = Lox()

    pylox_info = programinfo.ProgramInfo(
        name="Lox",
        version="0.1.0",
        docs_url="https://craftinginterpreters.com/"
    )

    args = loxcli.get_args()
    if args.is_verbose:
        loxcli.toggle_verbose(True)
    else:
        loxcli.toggle_verbose(False)

    if args.rpolish:
        lox.astprinter.rev_polish_notation = True

    if args.src:
        if not args.src.exists():
            print(f"[Error] Could not find file: '{args.src}'")
            sys.exit(64)
        lox.run_file(args.src)
    else:
        pylox_info.print()
        lox.run_prompt()


main()