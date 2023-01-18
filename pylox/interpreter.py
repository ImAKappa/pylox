"""interpreter.py

Module for Interpreter component of Lox interpreter
"""

# logs
from utils.ezlog import new_logger
logger = new_logger(__name__)
from rich import print as rprint
# app
from loxtoken import Token, TokenType
from expr import Expr, Binary, Unary, Literal, Grouping, Variable
import expr
from stmt import Expression, Print, Var
import stmt
from environment import Environment
# errors
from errors import Error

class LoxRuntimeError(Error):
    """Raise when runtime error occurs"""
    def __init__(self, token: Token, message: str):
        super().__init__(message)
        self.message = message
        self.token = token

class Interpreter(expr.Visitor, stmt.Visitor):
    """Interprets expressions"""

    def __init__(self):
        self.environment = Environment()

    def interpret(self, statements: list[stmt.Stmt]):
        try:
            for statement in statements:
                self.execute(statement)
        except LoxRuntimeError as e:
            raise

    def execute(self, statement: stmt.Stmt):
        statement.accept(self)
        return

    def stringify(self, obj):
        if obj is None: return "nil"

        if isinstance(obj, float):
            text = str(obj)
            if text.endswith(".0"):
                text = text[0:len(text) - 2]
            return text

        return f"'{str(obj)}'"

    def evaluate(self, expr: Expr):
        return expr.accept(self)

    # --- Statements

    def visit_expression(self, stmt: Expression):
        self.evaluate(stmt.expression)
        return

    def visit_print(self, stmt: Print) -> None:
        value = self.evaluate(stmt.expression)
        logger.info(self.stringify(value))
        return

    def visit_var(self, stmt: Var):
        value = None
        if (stmt.initializer is not None):
            value = self.evaluate(stmt.initializer)
        
        self.environment.define(stmt.name.lexeme, value)
        return

    # --- Expressions

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

    def visit_variable(self, expr: Variable):
        return self.environment.get(expr.name)

    # ---

    def is_equal(self, a, b):
        # if a is None and b is None: return True
        # if a is None: return False
        return a == b

    def check_number_operands(self, operator: Token, left, right):
        if not (isinstance(left, float) and isinstance(right, float)):
            raise LoxRuntimeError(operator, "Operands must be the numbers.")
        if right == 0:
            raise LoxRuntimeError(operator, "Division by Zero is not allowed")
        return

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