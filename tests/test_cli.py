from pathlib import Path
import io
import subprocess
import tempfile
from pylox.cli.loxcli import Args
from pylox import pylox

# def test_cli():
#     process = subprocess.Popen(["python", "-m", "pylox", "--src", "./fake923876508.txt"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     out, err = process.communicate()
#     assert out.decode("utf-8").strip() == "[Error] Could not find file: 'fake923876508.txt'"

# def test_debug_mode(capsys):

#     captured = capsys.readouterr()

def test_missing_src_file(capsys):
    args = Args(src=Path("./some-nonexistent-file.lox"), debug_on=False, rpolish=False)
    pylox.run(args)
    captured = capsys.readouterr()
    assert captured.err == f"[Error] Could not find file: '{args.src}'\n"
