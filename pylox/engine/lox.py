#!/usr/bin/env python3
"""lox.py

Main module for Lox interpreter
"""

# stdlib
from pathlib import Path
import io
import sys
# rich
from rich import print as rprint
# app
from engine.loxtoken import Token, TokenType
from cli.astprinter import AstPrinter
from engine.scanner import Scanner, ScannerError
from engine.loxparser import Parser, ParserError
from engine.interpreter import Interpreter, LoxRuntimeError
# logs
import logging
from utils.ezlog import new_logger
logger = new_logger(__name__)

class Lox:

    def __init__(self):
        self.had_error = False
        self.had_runtime_error = False
        self.interpreter = Interpreter()
        self.astprinter = AstPrinter()

    def report(self, line: int, where: str, message: str) -> None:
        # logger.error(f"[line {line}] Error {where}: {message}")
        rprint(f"[line {line}] Error {where}: {message}")
        self.had_error = True
        return

    def error(self, token: Token, message: str) -> None:
        if token.tokentype == TokenType.EOF:
            self.report(token.line, " at end", message)
        else:
            self.report(token.line, f"at '{token.lexeme}'", message)
        return

    def runtime_error(self, error: LoxRuntimeError):
        logger.error(f"[line {error.token.line}] {error.message}")
        self.had_runtime_error = True
        return

    def run(self, source: str, repl_mode = False) -> None:
        # Scan
        logger.debug("Creating Scanner")
        scanner = Scanner(source)
        try:
            logger.debug("Generating tokens")
            tokens = scanner.scan_tokens()
            scanner.log_tokens()
        except ScannerError as e:
            self.report(e.line, "", e.message)
            return
        finally:
            if self.had_error:
                return
        
        # Parse
        try:
            logger.debug("Creating parser")
            parser = Parser(tokens, repl_mode)
            logger.debug("Generating expression tree")
            statements = parser.parse()
        except ParserError as e:
            self.error(e.token, e.message)
        else:
            # logger.debug(self.astprinter.print(statements))
            pass
        finally:
            if self.had_error:
                return

        # Interpret
        try:
            logger.debug("Running interpreter")
            self.interpreter.interpret(statements)
        except LoxRuntimeError as e:
            self.runtime_error(e)
        return

    def run_file(self, file: Path):
        with io.open(file, mode="r") as f:
            source = f.read()
        self.run(source)
        if self.had_error: sys.exit(65)
        if self.had_runtime_error: sys.exit(70)
        return

    def print_prompt(self) -> None:
        rprint("[bold white]>[/bold white] ", end="")
        return

    def run_prompt(self):
        logger.debug("Starting prompt")
        while True:
            self.print_prompt()
            try:
                line = input()
                self.run(line, repl_mode=True)
                # Error shoudn't end interactive session
                self.had_error = False
                self.had_runtime_error = False
            except EOFError:
                break
        sys.exit(64)
        return