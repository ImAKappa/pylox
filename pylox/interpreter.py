import logging
from rich.logging import RichHandler
FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)
logger = logging.getLogger(__name__)

from errors import Error

from loxtoken import Token, TokenType
from tree import Visitor, Expr, Binary, Unary, Literal, Grouping

class InterpreterError(Error):
    """Rase when error occurs during iterpretation of syntax tree nodes"""
    def __init__(self, token: Token, message: str):
        super().__init__(message)
        self.message = message
        self.token = token

class InterpreterVisitor(Visitor):
    """Interprets expressions"""

    def visit_literal(self, expr: Literal):
        return expr.value

    def visit_grouping(self, expr: Grouping):
        return 