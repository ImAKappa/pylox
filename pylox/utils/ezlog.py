#!/usr/bin/env python3
"""ezlog.py

Utility for initializing a logger. 
This module extracts some of the boilerplate logger setup into a simple function.
"""

import logging
from rich.logging import RichHandler

def new_logger(name):
    FORMAT = "%(message)s"
    logging.basicConfig(
        level=logging.DEBUG, format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
    )
    logger = logging.getLogger(name)
    return logger