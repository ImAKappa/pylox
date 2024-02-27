"""interpreter.py

Module for Interpreter component of Lox interpreter
"""

# logs
from pylox.utils import new_logger
logger = new_logger(__name__)
from rich import print as rprint
# app
from pylox.engine.loxtoken import Token, TokenType
import pylox.engine.expr as expr
import pylox.engine.stmt as stmt
from pylox.engine.environment import Environment, BindingError, UninitializedError
# errors
from pylox.engine.errors import Error

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

    def evaluate(self, expr: expr.Expr):
        return expr.accept(self)

    # --- Statements

    def visit_expression(self, stmt: stmt.Expression) -> None:
        value = self.evaluate(stmt.expression)
        if self.repl_mode:
            rprint(self.stringify(value))
    
    def visit_if(self, stmt: stmt.If) -> None:
        if self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.then_branch)
        elif stmt.else_branch:
            self.execute(stmt.else_branch)

    def visit_print(self, stmt: stmt.Print) -> None:
        value = self.evaluate(stmt.expression)
        rprint(self.stringify(value))

    def visit_var(self, stmt: stmt.Var) -> None:
        value = None
        if stmt.initializer:
            value = self.evaluate(stmt.initializer)
        
        self.environment.define(stmt.name.lexeme, value)

    def visit_block(self, stmt: stmt.Block) -> None:
        self.execute_block(stmt.statements, Environment(self.environment))

    # ---

    def execute_block(self, statements: list[stmt.Stmt], environment: Environment) -> None:
        previous = self.environment
        try:
            self.environment = environment

            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous

    # --- Expressions

    def visit_literal(self, expr: expr.Literal) -> object:
        return expr.value

    def visit_grouping(self, expr: expr.Grouping) -> None:
        return self.evaluate(expr.expression)

    def is_truthy(self, obj) -> bool:
        # Only False and nil are False. Everything else is True
        if obj is None: return False
        if isinstance(obj, bool): return obj
        return True

    def check_number_operand(self, operator: Token, operand) -> None:
        if isinstance(operand, float): return
        raise LoxRuntimeError(operator, "Operand must be a number.")

    def visit_unary(self, expr: expr.Unary):
        right = self.evaluate(expr.right)

        match expr.operator.tokentype:
            case TokenType.MINUS:
                self.check_number_operand(expr.operator, right)
                return -float(right)
            case TokenType.BANG:
                return not self.is_truthy(right)

        # Unreachable
        return

    def visit_variable(self, expr: expr.Variable):
        return self.environment.get(expr.name)

    def visit_assign(self, expr: expr.Assign):
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
            raise LoxRuntimeError(operator, "Division by Zero is undefined")
        return

    def visit_binary(self, expr: expr.Binary):
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