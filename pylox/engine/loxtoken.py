"""loxtoken.py

Module for defining the valid tokens for Lox
"""

from dataclasses import dataclass
from enum import Enum, auto

# auto() assigns the constant with the enumerate value (0..len(TokenType))

class TokenType(Enum):
    # Single character tokens
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    COMMA = auto()
    DOT = auto()
    MINUS = auto()
    PLUS = auto()
    SEMICOLON = auto()
    SLASH = auto()
    STAR = auto()

    # One or two character tokens
    BANG = auto()
    BANG_EQUAL = auto()
    EQUAL = auto()
    EQUAL_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()

    # Literals
    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()

    # Keywords
    AND = auto()
    CLASS = auto()
    ELSE = auto()
    FALSE = auto()
    FUN = auto()
    FOR = auto()
    IF = auto()
    NIL = auto()
    OR = auto()
    PRINT = auto()
    RETURN = auto()
    SUPER = auto()
    THIS = auto()
    TRUE = auto()
    VAR = auto()
    WHILE = auto()

    # End of file
    EOF = auto()

@dataclass(frozen=True)
class Token:
    tokentype: TokenType
    lexeme: str
    literal: object
    line: int

    def __str__(self):
        return f"{self.tokentype} {self.lexeme} {self.lexeme}"