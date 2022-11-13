from pathlib import Path
import io
import logging
import sys

from loxtoken import Token, TokenType
from astprinter import AstPrinter
from scanner import Scanner, ScannerError
from parser import Parser, ParserError

from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class Lox:

    def __init__(self):
        self.had_error = False

    def report(self, line: int, where: str, message: str) -> None:
        logger.error(f"[line {line}] Error {where}: {message}")
        self.had_error = True
        return

    def error(self, token: Token, message: str) -> None:
        if token.tokentype == TokenType.EOF:
            self.report(token.line, " at end", message)
        else:
            self.report(token.line, f"at '{token.lexeme}'", message)
        return

    def run(self, source: str) -> None:
        logger.debug("Creating Scanner")
        scanner = Scanner(source)
        try:
            logger.debug("Generating tokens")
            tokens = scanner.scan_tokens()
        except ScannerError as e:
            self.report(e.line, "", e.message)
            return
        else:
            scanner.log_tokens(end=5)
        
        try:
            logger.debug("Creating parser")
            parser = Parser(tokens)
            logger.debug("Generating expression tree")
            expression = parser.parse()
        except ParserError as e:
            self.error(e.token, e.message)
        finally:
            if self.had_error: return

        logger.info(AstPrinter().print(expression))
        return

    def run_file(self, file: Path):
        with io.open(file, mode="r") as f:
            source = f.read()
        self.run(source)
        if self.had_error: sys.exit(64)
        return

    def run_prompt(self):
        logger.debug("Starting prompt")
        while True:
            print("> ", end="")
            try:
                line = input()
                self.run(line)
                # Error shoudn't end interactive session
                self.had_error = False
            except EOFError:
                break
        sys.exit(64)
        return