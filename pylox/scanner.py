import logging

from lox import Lox
from token import Token
from tokentype import TokenType

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class Scanner:
    def __init__(self, source: str):
        self.source = source
        self.tokens: list[Token] = []
        self.start = 0
        self.current = 0
        self.line = 1

    def is_at_end(self):
        return self.current >= len(self.source)

    def advance(self):
        self.curent += 1
        return self.source[self.current]

    def add_token(self, tokentype: TokenType, literal = None):
        text = self.source[self.start, self.current]
        self.tokens.append(Token(tokentype, text, literal, self.line))

    def scan_token(self):
        c = self.advance()
        match c:
            case '(': self.add_token(TokenType.LEFT_PAREN)
            case ')': self.add_token(TokenType.RIGHT_PAREN)
            case '{': self.add_token(TokenType.LEFT_BRACE)
            case '}': self.add_token(TokenType.RIGHT_BRACE)
            case ',': self.add_token(TokenType.COMMA)
            case '.': self.add_token(TokenType.DOT)
            case '-': self.add_token(TokenType.MINUS)
            case '+': self.add_token(TokenType.PLUS)
            case ';': self.add_token(TokenType.SEMICOLON)
            case '*': self.add_token(TokenType.STAR)
            case _:
                Lox().error(self.line, "Unexpected character.")
        return

    def scan_tokens(self):
        while not self.is_at_end():
            # At beginning of next lexeme
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens