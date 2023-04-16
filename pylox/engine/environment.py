"""environment.py

Module for defining environment of Lox interpreter, the place where variables and values live
"""

from pylox.engine.loxtoken import Token
# errors
from pylox.engine.errors import Error

class BindingError(Error):
    """Raise when runtime error occurs"""
    def __init__(self, token: Token, message: str):
        super().__init__(message)
        self.message = message
        self.token = token

class UninitializedError(Error):
    """Raise when accessing uninitialized variable"""
    def __init__(self, token: Token, message: str):
        super().__init__(message)
        self.message = message
        self.token = token

class Environment:

    def __init__(self, enclosing=None):
        self.enclosing: Environment = enclosing
        self.values: dict[str, object] = dict()

    def define(self, name: str, value: object):
        self.values[name] = value

    def assign(self, name: Token, value: object):
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return

        if self.enclosing:
            self.enclosing.assign(name, value)
            return
        
        raise BindingError(name, f"Undefined variable '{name.lexeme}'.") 

    def get(self, name: Token):
        if name.lexeme in self.values:
            value = self.values.get(name.lexeme)
            if value is None:
                raise UninitializedError(name, f"Uninitialized variable '{name.lexeme}'")
            return value

        if self.enclosing:
            return self.enclosing.get(name)

        raise BindingError(name, f"Undefined variable '{name.lexeme}'.")