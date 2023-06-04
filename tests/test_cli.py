from pathlib import Path
import io
import subprocess
import tempfile

def test_cli():
    process = subprocess.Popen(["python", "-m", "pylox", "--src", "./fake923876508.txt"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    assert out.decode("utf-8").strip() == "[Error] Could not find file: 'fake923876508.txt'"