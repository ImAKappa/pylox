"""scanner.py

Module for Scanner component of Lox Interpreter 
"""

# stdlib
from pylox.utils import new_logger
logger = new_logger(__name__)
# app modules
from pylox.engine.loxtoken import Token, TokenType
from pylox.engine.errors import Error

class ScannerError(Error):
    """Raise when error occurs during Scanning of source file"""
    def __init__(self, line: int, message: str):       
        super().__init__(message)
        self.message = message
        self.line = line

class Scanner:

    keywords = {
        "else": TokenType.ELSE,
        "false": TokenType.FALSE,
        "for": TokenType.FOR,
        "fun": TokenType.FUN,
        "if": TokenType.IF,
        "nil": TokenType.NIL,
        "or": TokenType.OR,
        "print": TokenType.PRINT,
        "return": TokenType.RETURN,
        "super": TokenType.SUPER,
        "this": TokenType.THIS,
        "true": TokenType.TRUE,
        "var": TokenType.VAR,
        "while": TokenType.WHILE,
    }

    def __init__(self, source: str):
        self.source = source
        logger.info(f"{source=}\n{len(source)=}")
        self.tokens: list[Token] = []
        self.start = 0
        self.current = 0
        self.line = 1

    def is_at_end(self):
        return self.current >= len(self.source)

    def advance(self):
        c = self.source[self.current]
        self.current += 1
        return c

    def add_token(self, tokentype: TokenType, literal=None):
        text = self.source[self.start:self.current]
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

    def peek_next(self):
        if self.current + 1 >= len(self.source): return '\0'
        return self.source[self.current + 1]

    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n': self.line += 1
            self.advance()

        if self.is_at_end():
            raise ScannerError(self.line, "Unterminated string.")

        # The closing ".
        self.advance()

        # Trim the surrounding quotes
        value = self.source[self.start+1:self.current-1]
        self.add_token(TokenType.STRING, value)
        # UPDATE: Support for escape sequences

    def is_digit(self, c: str):
        return c.isnumeric()

    def number(self):
        while self.is_digit(self.peek()):
            self.advance()
        
        # Look for fractional part
        if self.peek() == '.' and self.is_digit(self.peek_next()):
            # Consume the "."
            self.advance()

            while self.is_digit(self.peek()): self.advance()

        self.add_token(TokenType.NUMBER, float(self.source[self.start:self.current]))

    def is_alpha(self, c: str):
        return c.isalpha() or c == '_'

    def is_alphanumeric(self, c: str):
        return self.is_alpha(c) or self.is_digit(c)

    def identifier(self):
        while self.is_alphanumeric(self.peek()): self.advance()
        
        text = self.source[self.start:self.current]
        type = self.keywords.get(text)
        if type is None: type = TokenType.IDENTIFIER
        self.add_token(type)

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
            case '!': self.add_token(TokenType.BANG_EQUAL if self.match('=') else TokenType.BANG)
            case '=': self.add_token(TokenType.EQUAL_EQUAL if self.match('=') else TokenType.EQUAL)
            case '<': self.add_token(TokenType.LESS_EQUAL if self.match('=') else TokenType.LESS)
            case '>': self.add_token(TokenType.GREATER_EQUAL if self.match('=') else TokenType.GREATER)
            case '/':
                if self.match('/'):
                    # A comment goes until the end of the line.
                    while (self.peek() != '\n' and not self.is_at_end()):
                        self.advance()
                elif self.match('*'):
                    # A block comment goes until a closing '*/'
                    while (not (self.peek() == '*' and self.peek_next() == '/') and not self.is_at_end()):
                        self.advance()
                    if not self.is_at_end():
                        self.match('*')
                        self.match('/')
                    else:
                        raise ScannerError(self.line, f"Unterminated block comment")
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
                if self.is_digit(c):
                    self.number()
                elif self.is_alpha(c):
                    self.identifier()
                else:
                    raise ScannerError(self.line, f"Unexpected character: {c}")
        return

    def scan_tokens(self):
        while not self.is_at_end():
            # At beginning of next lexeme
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def log_tokens(self, start: int=None, end: int=None) -> None:
        start = 0 if start is None else start
        end = len(self.tokens) if end is None else min(end, len(self.tokens))
        logger.info(f"Tokens {start} to {end}:")
        for token in self.tokens[start:end]:
            logger.info(f"\t{repr(token)}")
        return