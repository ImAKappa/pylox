"""pylox.py

Main module for running the pylox application
"""

import pylox.cli.loxcli as loxcli
from pylox.pylox import run

def main():
    args = loxcli.get_args()
    run(args)
    
main()