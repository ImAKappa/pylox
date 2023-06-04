"""
Script that automatically runs the Lox interpreter on each of the loxtest source files
"""

# Run tests by directory
# Report which directories (and source files) fail

# Note: Each test file also contains the expected output

from pathlib import Path
import io
import subprocess

def clean_out(out: bytes):
    """"""
    program_out = out.decode("utf-8").strip()
    if "expect:" in program_out:
        return program_out.replace("'", "").splitlines()
    return program_out.splitlines()

def parse_expected(fp: Path):
    with io.open(fp, mode="r") as f:
        content = f.readlines()
    expected = list()
    for line in content:
        if "expect: " in line:
            _, expect = line.strip().split("expect: ")
            expected.append(expect)
        if "Error at" in line:
            expect = line.strip().replace("// ", "")
            expected.append(expect)
    return expected

if __name__ == "__main__":
    app = Path('./pylox/pylox.py')
    fp = Path('./loxtests/print/missing_argument.lox')
    process = subprocess.Popen(['python', str(app), '--src', fp], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    # program_out = clean_out(out)
    program_out = out
    expected_out = parse_expected(fp)

    print(f"Testing {str(fp)}")
    print()
    passes = 0
    for program, expect in zip(program_out, expected_out):
        print(program_out)
        print(expected_out)

        if program == expect:
            print("PASS")
            passes += 1
        else:
            print(f"FAIL ... {program=} != {expect=}")
    print()
    # pass_rate = passes/len(expected_out) * 100.
    # print(f"{passes}/{len(expected_out)} test cases passed. ({pass_rate}%)")