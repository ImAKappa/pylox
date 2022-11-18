#!/usr/bin/env python3
"""ezlog.py

Utility for initializing a logger. 
This module extracts some of the boilerplate logger setup into a simple function.
"""

import logging
from rich.logging import RichHandler

def new_logger(name, global_loglevel=logging.WARNING):
    FORMAT = "%(message)s"
    logging.basicConfig(
        level=global_loglevel, format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
    )
    logger = logging.getLogger(name)
    if name == "__main__":
        print(name)
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(global_loglevel)
    return logger