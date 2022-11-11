import logging
from rich.logging import RichHandler
FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)
logger = logging.getLogger(__name__)


from loxtoken import Token, TokenType
from tree import Expr, Binary, Unary, Literal, Grouping

class Parser:

    def __init__(self):
        self.tokens: list[Token] = []
        self.current = 0

    def peek(self) -> Token:
        return self.tokens[self.current]

    def is_at_end(self) -> bool:
        return self.peek().type == TokenType.EOF
    
    def previous(self) -> Token:
        return self.tokens[self.current-1]

    def advance(self) -> Token:
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def check(self, type: TokenType) -> bool:
        if self.is_at_end(): return False
        return self.peek().type == type

    def match(self, *types: list[TokenType]) -> bool:
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False

    def primary(self):
        if self.match(TokenType.FALSE): return Literal(False)
        if self.match(TokenType.TRUE): return Literal(True)
        if self.match(TokenType.NIL): return Literal(None)

        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.previous().literal)

        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)
        

    def unary(self):
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator: Token = self.previous()
            right = self.unary()
            return Unary(operator, right)
        return self.primary()

    def factor(self):
        expr: Expr = self.unary()

        while self.match(TokenType.STAR, TokenType.SLASH):
            operator: TokenType = self.previous()
            right: Expr = self.unary()
            expr = Binary(expr, operator, right)
        return expr

    def term(self):
        expr: Expr = self.factor()

        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator: TokenType = self.previous()
            right: Expr = self.factor()
            expr = Binary(expr, operator, right)
        return expr

    def comparison(self):
        expr: Expr = self.term()

        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator: Token = self.previous()
            right: Expr = self.term()
            expr = Binary(expr, operator, right)
        return expr

    def equality(self) -> Expr:
        expr = self.comparison()

        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator: Token = self.previous()
            right: Expr = self.comparison()
            expr = Binary(expr, operator, right)
        return expr

    def expression(self) -> Expr:
        return self.equality()