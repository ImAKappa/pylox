from pathlib import Path
import io
import subprocess

def test_cli():
    app = Path('./pylox/pylox.py')
    process = subprocess.Popen(['python', str(app), '--src ./fake.txt'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    assert out == "Could not find file"