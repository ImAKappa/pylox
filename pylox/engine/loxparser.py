"""loxparser.py

Module for parsing lox tokens into an AST
"""

# logs
from pylox.utils import new_logger
logger = new_logger(__name__)

from pylox.engine.errors import Error

from pylox.engine.loxtoken import Token, TokenType
from pylox.engine.expr import Expr, Binary, Unary, Literal, Grouping, Variable, Assign
from pylox.engine.stmt import Stmt
import pylox.engine.stmt as stmt

class ParserError(Error):
    """Rase when error occurs during Parsing of tokens"""
    def __init__(self, token: Token, message: str):       
        super().__init__(message)
        self.message = message
        self.token = token

class Parser:

    def __init__(self, tokens: list[Token], repl_mode: bool):
        self.tokens = tokens
        self.current = 0
        self.repl_mode = repl_mode

    def parse(self) -> list[Stmt]:
        statements = list()
        while (not self.is_at_end()):
            statements.append(self.declaration())
        return statements

    def declaration(self) -> Stmt:
        try:
            if self.match(TokenType.VAR): return self.var_declaration()
            return self.statement()
        except ParserError as e:
            self.synchronize()
            raise
            
    def var_declaration(self):
        name: Token = self.consume(TokenType.IDENTIFIER, "Expect variable name")

        initializer: Expr = None
        if self.match(TokenType.EQUAL):
            initializer = self.expression()

        self.consume(TokenType.SEMICOLON, "Expect ';' after variable declaration")
        return stmt.Var(name, initializer)

    def statement(self) -> Stmt:
        if self.match(TokenType.IF): return self.if_stmt()
        if self.match(TokenType.PRINT): return self.print_stmt()
        if self.match(TokenType.LEFT_BRACE): return stmt.Block(self.block())
        return self.expr_stmt()
    
    def if_stmt(self) -> Stmt:
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'if'.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after if condition.")

        then_branch = self.statement()
        else_branch = None
        if self.match(TokenType.ELSE):
            else_branch = self.statement()

        return stmt.If(condition, then_branch, else_branch)

    def print_stmt(self) -> Stmt:
        value: Expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return stmt.Print(value)

    def block(self):
        statements: list[Stmt] = list()
        while not self.check(TokenType.RIGHT_BRACE) and not self.is_at_end():
            statements.append(self.declaration())

        self.consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
        return statements

    def expr_stmt(self):
        value: Expr = self.expression()
        if not self.repl_mode:
            self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return stmt.Expression(value)

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

    def consume(self, toktype: TokenType, message: str):
        if self.check(toktype):
            return self.advance()
        else:
            raise self.error(self.peek(), message)

    def primary(self):
        if self.match(TokenType.FALSE): return Literal(False)
        if self.match(TokenType.TRUE): return Literal(True)
        if self.match(TokenType.NIL): return Literal(None)
        if self.match(TokenType.IDENTIFIER): return Variable(self.previous())

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
        return self.assignment()

    def assignment(self) -> Expr:
        expr = self.equality()

        if self.match(TokenType.EQUAL):
            equals: Token = self.previous()
            value: Expr = self.assignment()

            if isinstance(expr, Variable):
                name: Token = expr.name
                return Assign(name, value)
            
            self.error(equals, "Invalid assignment target")
        return expr