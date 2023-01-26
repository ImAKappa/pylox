"""pylox.py

Main module for running the pylox application
"""

import sys
from cli import loxcli, programinfo
from engine.lox import Lox

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

    if args.src:
        if not args.src.exists():
            print("Could not find file")
            sys.exit(64)
        lox.run_file(args.src)
    else:
        pylox_info.print()
        lox.run_prompt()


if __name__ == "__main__":
    main()