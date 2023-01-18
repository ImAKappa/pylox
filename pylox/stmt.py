"""stmt.py

Module for defining Lox statments
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from loxtoken import Token
from expr import Expr

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

    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor: Visitor):
        return visitor.visit_print(self)

@dataclass
class Expression(Stmt):

    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor: Visitor):
        return visitor.visit_expression(self)