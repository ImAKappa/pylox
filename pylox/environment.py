"""environment.py

Module for defining environment of Lox interpreter, the place where variables and values live
"""

from loxtoken import Token
# errors
from errors import Error

class BindingError(Error):
    """Raise when runtime error occurs"""
    def __init__(self, token: Token, message: str):
        super().__init__(message)
        self.message = message
        self.token = token


class Environment:

    def __init__(self):
        self.values: dict[str, object] = dict()

    def define(self, name: str, value: object):
        self.values[name] = value

    def get(self, name: Token):
        if (name in self.values.keys()):
            return self.values.get(name.lexeme)

        raise BindingError(name, f"Undefined variable '{name.lexeme}'.")