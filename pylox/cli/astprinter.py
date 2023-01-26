"""astprinter.py

Module for printing the Abstract Syntax Tree
"""

# TODO: Update to handle Statements and not just Expressions

from engine.loxtoken import Token, TokenType
from engine.expr import Visitor, Expr, Binary, Grouping, Literal, Unary, Variable, Assign

class AstPrinter(Visitor):

    def print(self, expr: Expr):
        return expr.accept(self)

    def parenthesize(self, name: str, *exprs: list[Expr]):
        out = f"({name}"
        for expr in exprs:
            out += " "
            out += expr.accept(self)
        out += ")"
        return out

    def visit_binary(self, expr: Binary):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_grouping(self, expr: Grouping):
        return self.parenthesize("group", expr.expression)

    def visit_literal(self, expr: Literal):
        return str(expr.value) if expr.value else "nil"

    def visit_unary(self, expr: Unary):
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def visit_variable(self, expr: Variable):
        return str(expr.name)

    def visit_assign(self, expr: Assign):
        return self.parenthesize("=", expr.name.lexeme, expr.value)

if __name__ == "__main__":
    expression: Expr = Binary(
        Unary(Token(TokenType.MINUS, "-", None, 1), Literal(123)),
        Token(TokenType.STAR, "*", None, 1),
        Grouping(Literal(45.67))
    )

    print(AstPrinter().print(expression))