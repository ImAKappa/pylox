"""programinfo.py

Module for templating the program information
"""

from dataclasses import dataclass
from rich.console import Console
from rich.text import Text

@dataclass
class ProgramInfo:
    name: str
    version: str
    docs_url: str

    def __str__(self):
        return f"{self.name} {self.version} | Docs: {self.docs_url}"

    def print(self) -> None:
        console = Console()
        text = Text.assemble(
            (self.name, "bold blue"),
            (" "),
            (self.version),
            (" | "),
            (f"Docs: '{self.docs_url}'", "green")
        )
        console.print(text)
        return
    