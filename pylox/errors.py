"""errors.py

Module for defining errors scoped to this application
"""

class Error(Exception):
    """Base-class for interpreter errors"""
    def __init__(self, message: str):       
        super().__init__(message)
        self.message = message