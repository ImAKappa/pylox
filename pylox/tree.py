import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from loxtoken import Token

from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

logger = logging.getLogger(__name__)

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