import logging
from rich.logging import RichHandler
FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)
logger = logging.getLogger(__name__)

from errors import Error

from loxtoken import Token, TokenType
from tree import Expr, Binary, Unary, Literal, Grouping

class ParserError(Error):
    """Rase when error occurs during Parsing of tokens"""
    def __init__(self, token: Token, message: str):       
        super().__init__(message)
        self.message = message
        self.token = token

class Parser:

    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        return self.expression()

    def peek(self) -> Token:
        return self.tokens[self.current]

    def is_at_end(self) -> bool:
        return self.peek().tokentype == TokenType.EOF
    
    def previous(self) -> Token:
        return self.tokens[self.current-1]

    def error(self, token: Token, message: str):
        return ParserError(token, message)

    def synchronize(self):
        self.advance()

        while not self.is_at_end():
            if self.previous().tokentype == TokenType.SEMICOLON: return

            match self.peek().tokentype:
                case TokenType.CLASS | TokenType.FUN | TokenType.VAR \
                    | TokenType.FOR | TokenType.IF | TokenType.WHILE \
                    | TokenType.PRINT \
                    | TokenType.RETURN:
                    return

            self.advance()
                    
    def advance(self) -> Token:
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def check(self, type: TokenType) -> bool:
        if self.is_at_end(): return False
        return self.peek().tokentype == type

    def match(self, *types: list[TokenType]) -> bool:
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False

    def consume(self, type: TokenType, message: str):
        if self.check(type): return self.advance()

        raise self.error(self.peek(), message)

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

        raise self.error(self.peek(), "Expect expression.")

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