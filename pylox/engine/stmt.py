"""stmt.py

Module for defining Lox statments
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pylox.engine.loxtoken import Token
from pylox.engine.expr import Expr

class Visitor:

    @abstractmethod
    def visit_block(self, stmt):
        pass

    @abstractmethod
    def visit_class(self, stmt):
        pass

    @abstractmethod
    def visit_expression(self, stmt):
        pass

    @abstractmethod
    def visit_function(self, stmt):
        pass

    @abstractmethod
    def visit_if(self, stmt):
        pass

    @abstractmethod
    def visit_print(self, stmt):
        pass

    @abstractmethod
    def visit_return(self, stmt):
        pass

    @abstractmethod
    def visit_var(self, stmt):
        pass

    @abstractmethod
    def visit_while(elf, stmt):
        pass


class Stmt(ABC):
    @abstractmethod
    def accept(self, visitor: Visitor):
        pass

@dataclass
class Print(Stmt):
    expression: Expr

    def accept(self, visitor: Visitor):
        return visitor.visit_print(self)

@dataclass
class Expression(Stmt):
    expression: Expr

    def accept(self, visitor: Visitor):
        return visitor.visit_expression(self)

@dataclass
class Var(Stmt):
    name: Token
    initializer: Expr

    def accept(self, visitor: Visitor):
        return visitor.visit_var(self)

@dataclass
class Block(Stmt):
    statements: list[Stmt]

    def accept(self, visitor: Visitor):
        return visitor.visit_block(self)
    
@dataclass
class If(Stmt):
    condition: Expr
    then_branch: Stmt
    else_branch: Stmt

    def accept(self, visitor: Visitor):
        return visitor.visit_if(self)