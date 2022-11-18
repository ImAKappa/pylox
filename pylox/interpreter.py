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

class LoxRuntimeError(Error):
    """Raise when runtime error occurs"""
    def __init__(self, token: Token, message: str):
        super().__init__(message)
        self.message = message
        self.token = token

class Interpreter(Visitor):
    """Interprets expressions"""

    def __init__(self):
        pass

    def interpret(self, expression):
        try:
            value = self.evaluate(expression)
            logger.info(self.stringify(value))
        except LoxRuntimeError as e:
            raise

    def stringify(self, obj):
        if obj is None: return "nil"

        if isinstance(obj, float):
            text = str(obj)
            if text.endswith(".0"):
                text = text[0, len(text) - 2]
            return text

        return str(obj)

    def evaluate(self, expr: Expr):
        return expr.accept(self)

    def visit_literal(self, expr: Literal):
        return expr.value

    def visit_grouping(self, expr: Grouping):
        return self.evaluate(expr.expression)

    def is_truthy(self, obj):
        # Only False and nil are False. Everything else is True
        if obj is None: return False
        if isinstance(obj, bool): return obj
        return True

    def check_number_operand(self, operator: Token, operand):
        if isinstance(operand, float): return
        raise LoxRuntimeError(operator, "Operand must be a number.")

    def visit_unary(self, expr: Unary):
        right = self.evaluate(expr.right)

        match expr.operator.tokentype:
            case TokenType.MINUS:
                self.check_number_operand(expr.operator, right)
                return -float(right)
            case TokenType.BANG:
                return not self.is_truthy(right)

        # Unreachable
        return

    def is_equal(self, a, b):
        # if a is None and b is None: return True
        # if a is None: return False
        return a == b

    def check_number_operands(self, operator: Token, left, right):
        if isinstance(left, float) and isinstance(right, float): return
        raise LoxRuntimeError(operator, "Operands must be the numbers.")

    def visit_binary(self, expr: Binary):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        match expr.operator.tokentype:
            case TokenType.GREATER:
                self.check_number_operands(expr.operator, left, right)
                return float(left) > float(right)
            case TokenType.GREATER_EQUAL:
                self.check_number_operands(expr.operator, left, right)
                return float(left) >= float(right)
            case TokenType.LESS:
                self.check_number_operands(expr.operator, left, right)
                return float(left) < float(right)
            case TokenType.LESS_EQUAL:
                self.check_number_operands(expr.operator, left, right)
                return float(left) <= float(right)
            case TokenType.BANG_EQUAL:
                return not self.is_equal(left, right)
            case TokenType.EQUAL_EQUAL:
                return self.is_equal(left, right)
            case TokenType.MINUS:
                self.check_number_operands(expr.operator, left, right)
                return float(left) - float(right)
            case TokenType.PLUS:
                if isinstance(left, float) and isinstance(right, float):
                    return left + right
                if isinstance(left, str) and isinstance(right, str):
                    return left + right
                raise LoxRuntimeError(expr.operator, "Operands must be two numbers or two strings")
            case TokenType.SLASH:
                self.check_number_operands(expr.operator, left, right)
                return float(left) / float(right)
            case TokenType.STAR:
                self.check_number_operands(expr.operator, left, right)
                return float(left) * float(right)

        # Unreachable
        return