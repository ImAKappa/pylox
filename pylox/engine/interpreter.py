"""interpreter.py

Module for Interpreter component of Lox interpreter
"""

# logs
from utils.ezlog import new_logger
logger = new_logger(__name__)
from rich import print as rprint
# app
from engine.loxtoken import Token, TokenType
from engine.expr import Expr, Binary, Unary, Literal, Grouping, Variable, Assign
import engine.expr as expr
from engine.stmt import Expression, Print, Var, Block
import engine.stmt as stmt
from engine.environment import Environment, BindingError, UninitializedError
# errors
from engine.errors import Error

class LoxRuntimeError(Error):
    """Raise when runtime error occurs"""
    def __init__(self, token: Token, message: str):
        super().__init__(message)
        self.message = message
        self.token = token

class Interpreter(expr.Visitor, stmt.Visitor):
    """Interprets expressions"""
    # TODO: Evaluate expressions in REPL mode

    def __init__(self, repl_mode: bool):
        self.environment = Environment()
        self.repl_mode = repl_mode

    def interpret(self, statements: list[stmt.Stmt]):
        try:
            for statement in statements:
                self.execute(statement)
        except BindingError as e:
            raise LoxRuntimeError(e.token, e.message)
        except UninitializedError as e:
            raise LoxRuntimeError(e.token, e.message)
        except LoxRuntimeError as e:
            raise

    def execute(self, statement: stmt.Stmt):
        statement.accept(self)
        return

    def stringify(self, obj):
        # Markup [x]...[/x] is based on Rich text formatting: https://rich.readthedocs.io/en/stable/style.html
        # colours are based on https://craftinginterpreters.com/the-lox-language.html
        if obj is None: return "[blue]nil[/blue]"

        if isinstance(obj, float):
            text = str(obj)
            if text.endswith(".0"):
                text = text[0:len(text) - 2]
            return f"[dark_orange3]{text}[dark_orange3]"

        if isinstance(obj, bool):
            text = str(obj)
            return f"[deep_sky_blue1]{text.lower()}[/deep_sky_blue1]"

        return f"[gold3]'{obj}'[/gold3]"

    def evaluate(self, expr: Expr):
        return expr.accept(self)

    # --- Statements

    def visit_expression(self, stmt: Expression):
        value = self.evaluate(stmt.expression)
        if self.repl_mode:
            rprint(self.stringify(value))
        return

    def visit_print(self, stmt: Print) -> None:
        value = self.evaluate(stmt.expression)
        rprint(self.stringify(value))
        return

    def visit_var(self, stmt: Var):
        value = None
        if stmt.initializer:
            value = self.evaluate(stmt.initializer)
        
        self.environment.define(stmt.name.lexeme, value)
        return

    def visit_block(self, stmt: Block):
        self.execute_block(stmt.statements, Environment(self.environment))
        return

    # ---

    def execute_block(self, statements: list[stmt.Stmt], environment: Environment):
        previous = self.environment
        try:
            self.environment = environment

            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous
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

    def visit_assign(self, expr: Assign):
        value = self.evaluate(expr.value)
        self.environment.assign(expr.name, value)
        return value

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