"""astprinter.py

Module for printing the Abstract Syntax Tree
"""

# TODO: Update to handle Statements and not just Expressions

from pylox.engine.loxtoken import Token, TokenType
from pylox.engine.expr import Visitor, Expr, Binary, Grouping, Literal, Unary, Variable, Assign
import pylox.engine.expr as expr
from pylox.engine.stmt import Stmt, Expression
import pylox.engine.stmt as stmt

class AstPrinter(expr.Visitor, stmt.Visitor):

    def __init__(self, rev_polish_notation=False):
        """rpn (Reverse Polish Notation)"""
        self.rev_polish_notation = rev_polish_notation

    def print(self, expr: Expr | Stmt):
        return expr.accept(self)

    def parenthesize(self, name: str, *exprs: list[Expr]):
        if self.rev_polish_notation:
            out = ""
            for expr in exprs:
                out += expr.accept(self)
                out += " "
            out += name
        else:
            out = f"({name}"
            for expr in exprs:
                out += " "
                out += expr.accept(self)
            out += ")"
        return out

    # --- statements
    def visit_expression(self, stmt: Expression):
        return stmt.expression.accept(self)

    # --- expressions

    def visit_binary(self, expr: Binary):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_grouping(self, expr: Grouping):
        return self.parenthesize("group", expr.expression)

    def visit_literal(self, expr: Literal):
        if isinstance(expr.value, bool):
            return f"'{str(expr.value).lower()}'"
        if expr.value:
            return f"'{expr.value}'"
        return "'nil'"

    def visit_unary(self, expr: Unary):
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def visit_variable(self, expr: Variable):
        return f"'{expr.name.lexeme}'"

    def visit_assign(self, expr: Assign):
        return self.parenthesize("=", expr.value)

if __name__ == "__main__":
    expression: Expr = Binary(
        Unary(Token(TokenType.MINUS, "-", None, 1), Literal(123)),
        Token(TokenType.STAR, "*", None, 1),
        Grouping(Literal(45.67))
    )

    print(AstPrinter().print(expression))