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
        self.current += 1
        return self.source[self.current]    

    def add_token(self, tokentype: TokenType, literal=None):
        text = self.source[self.start, self.current]
        self.tokens.append(Token(tokentype, text, literal, self.line))

    def match(self, expected: str):
        """Conditional advance; depends on if the advance char matches expected"""
        if self.is_at_end(): return False
        if self.source[self.current] != expected: return False
        self.current += 1
        return True

    def peek(self):
        if self.is_at_end(): return '\0'
        return self.source[self.current]

    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n': self.line += 1
            self.advance()

        if self.is_at_end():
            Lox().error(self.line, "Unterminated string.")
            return

        # The closing ".
        self.advance()

        # Trim the surrounding quotes
        value = self.source[self.start+1:self.current-1]
        self.add_token(TokenType.STRING, value)
        # UPDATE: Support for escape sequences

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
            case '!': self.add_token(TokenType.BANG_EQUAL if self.match('=') else TokenType.EQUAL)
            case '=': self.add_token(TokenType.EQUAL_EQUAL if self.match('=') else TokenType.EQUAL)
            case '<': self.add_token(TokenType.LESS_EQUAL if self.match('=') else TokenType.LESS)
            case '>': self.add_token(TokenType.GREATER_EQUAL if self.match('=') else TokenType.GREATER)
            case '/':
                if self.match('/'):
                    # A comment goes until the end of the line.
                    while (self.peek() != '\n' and not self.is_at_end()):
                        self.advance()
                else:
                    self.add_token(TokenType.SLASH)
            case ' ' | '\r' | '\t':
                # Ignore whitespace
                pass
            case '\n':
                self.line += 1
            case '"':
                self.string()
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