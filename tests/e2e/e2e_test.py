import math
import json
from pathlib import Path
import subprocess
import tempfile


script_path = str((Path(__file__).parent.parent.parent/'src/octanexchange/exrates.py').resolve())


def test_history():
    f = None
    try:
        f = tempfile.NamedTemporaryFile(suffix='.jsonl', delete=False)
        cmd = [
            "python", 
            script_path, 
            "history", 
            "--start", 
            "2021-03-01", 
            "--end", 
            "2021-03-02", 
            "--base", 
            "EUR", 
            "--symbol", 
            "USD", 
            "CAD", 
            "--output",
            f.name,
        ]
        subprocess.run(cmd)

        json_lines = f.readlines()
        actual = set(tuple(json.loads(json_str).items()) for json_str in json_lines)
        expected = set(tuple(d.items()) for d in [
            {"date": "2021-03-01", "base": "EUR", "symbol": "CAD", "rate": 1.5274},
            {"date": "2021-03-01", "base": "EUR", "symbol": "USD", "rate": 1.2053},
            {"date": "2021-03-02", "base": "EUR", "symbol": "CAD", "rate": 1.5225},
            {"date": "2021-03-02", "base": "EUR", "symbol": "USD", "rate": 1.2028}
        ])
        assert actual == expected
    finally:
        if f is not None: f.close()


def test_history_empty():
    # This is different than a unit test for the same situation because a networking
    # library raises an error when the response is empty.
    f = None
    try:
        f = tempfile.NamedTemporaryFile(suffix='.jsonl', delete=False)
        cmd = [
            "python", 
            script_path, 
            "history", 
            "--start", 
            "2022-02-19", 
            "--end", 
            "2022-02-19", 
            "--symbol", 
            "CAD", 
            "--output",
            f.name,
        ]
        subprocess.run(cmd)

        json_lines = f.readlines()
        assert len(json_lines) == 0
    finally:
        if f is not None: f.close()


def test_convert():
    cmd = ["python", script_path, "convert", "--date", "2021-03-01", "--base", "EUR", "--symbol", "USD", "--amount", "10"]
    out = subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode('utf-8')

    expected_amount = 12.053
    float_out = float(out.strip())

    assert math.isclose(float_out, expected_amount, abs_tol=0.1)
