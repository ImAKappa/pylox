"""expr.py

Module for defining Expression nodes in the Lox AST 
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from engine.loxtoken import Token

class Visitor(ABC):
    
    @abstractmethod
    def visit_binary(self, expr):
        pass

    @abstractmethod
    def visit_grouping(self, expr):
        pass

    @abstractmethod
    def visit_literal(self, expr):
        pass

    @abstractmethod
    def visit_unary(self, expr):
        pass

    @abstractmethod
    def visit_variable(self, expr):
        pass

    @abstractmethod
    def visit_assign(self, expr):
        pass

class Expr(ABC):
    @abstractmethod
    def accept(self, visitor: Visitor):
        pass

@dataclass
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr

    def accept(self, visitor: Visitor):
        return visitor.visit_binary(self)

@dataclass
class Grouping(Expr):
    expression: Expr

    def accept(self, visitor: Visitor):
        return visitor.visit_grouping(self)

@dataclass
class Literal(Expr):
    value: object

    def accept(self, visitor: Visitor):
        return visitor.visit_literal(self)

@dataclass
class Unary(Expr):
    operator: Token
    right: Expr

    def accept(self, visitor: Visitor):
        return visitor.visit_unary(self)

@dataclass
class Variable(Expr):
    name: Token

    def accept(self, visitor: Visitor):
        return visitor.visit_variable(self)

@dataclass
class Assign(Expr):
    name: Token
    value: Expr

    def accept(self, visitor: Visitor):
        return visitor.visit_assign(self)