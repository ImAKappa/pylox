import sys
import logging

from lox import Lox

num_args = len(sys.argv)
args = sys.argv

logger = logging.getLogger('pylox')
logger.setLevel(logging.DEBUG)

lox = Lox()

if __name__ == "__main__":

    if num_args > 2:
        logger.info("Usage: pylox [script]")
        sys.exit(64)
    if num_args == 2:
        lox.run_file(args[1])
    else:
        lox.run_prompt()
