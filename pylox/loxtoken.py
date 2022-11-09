from dataclasses import dataclass

from tokentype import TokenType

@dataclass(frozen=True)
class Token:
    tokentype: TokenType
    lexeme: str
    literal: object
    line: int

    def __str__(self):
        return f"{self.tokentype} {self.lexeme} {self.lexeme}"