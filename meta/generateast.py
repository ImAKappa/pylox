import argparse
from pathlib import Path
import io
from dataclasses import dataclass

@dataclass
class Field:
    name: str
    type: str

@dataclass
class AstNode:
    classname: str
    params: list[Field]


ast = [
    AstNode("Binary", [Field("left", "Expr")])
]


def define_ast(ast: list[AstNode]):
    return NotImplemented


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--out", help="Output directory")
    args = parser.parse_args()
    
    output_dir = Path(args.out)
    output_file = output_dir/Path("expr.py")

    try:
        with io.open(output_file, mode="w") as f:
            f.write("Hello")
    except FileNotFoundError as e:
        print(e)