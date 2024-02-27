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

# TODO: Figure out a way to provide interactive input:
# See https://stackoverflow.com/questions/41194262/how-can-i-make-py-test-tests-accept-interactive-input?rq=4
# def test_debug_mode(capsys):
#     args = Args(src=None, debug=True, rpolish=False)
#     pylox.run(args)
#     captured = capsys.readouterr()
#     assert "DEBUG" in captured.out

def test_missing_src_file(capsys):
    args = Args(src=Path("./some-nonexistent-file.lox"), debug=False, rpolish=False)
    pylox.run(args)
    captured = capsys.readouterr()
    assert captured.err == f"[Error] Could not find file: '{args.src}'\n"
