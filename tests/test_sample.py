from pathlib import Path
from pylox.cli.loxcli import Args
from pylox import pylox

# TODO: Parse expected values from comments in files
def parse_expected(file: Path) -> str:
    # Read line by line (what if multiline?) and look for [expect] [error kind] [colon (:)] [expected]
    pass

def test_number_src_file(capsys):
    args = Args(src=Path("./tests/samples/operator/add.lox"), debug=False, rpolish=False)
    pylox.run(args)
    captured = capsys.readouterr().out
    actual = captured.splitlines()
    expected = ["579", "'string'"]
    assert actual == expected
