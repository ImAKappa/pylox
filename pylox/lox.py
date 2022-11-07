from pathlib import Path
import io
import logging
import sys

from scanner import Scanner

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class Lox:

    def __init__(self):
        self.had_error = False

    def report(self, line: int, where: str, message: str):
        logger.error(f"[line {line}] Error {where}: {message}")
        self.had_error = True
        return

    def error(self, line: int, message: str):
        self.report(line, "", message)
        return

    def run(self, source: str):
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        for token in tokens:
            logger.info(repr(token))
        return

    def run_file(self, file: Path):
        with io.open(file, mode="r") as f:
            source = f.read()
        self.run(source)
        if self.had_error: sys.exit(64)
        return

    def run_prompt(self):
        while True:
            print("> ", end="")
            try:
                line = input()
                print(line)
                self.run(line)
                # Error shoudn't end interactive session
                self.had_error = False
            except EOFError:
                break
        sys.exit(64)
        return