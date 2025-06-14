import json
import os
import subprocess
import tempfile

import pytest


def test_plugin_logs_expected_results():
    with tempfile.TemporaryDirectory() as tmpdir:
        output_file = os.path.join(tmpdir, "report.json")

        result = subprocess.run(
            [
                "poetry", "run", "pytest",
                "tests/dummy_tests",
                "--capture-screenshots=none",
                f"--json-report={output_file}"
            ],
            capture_output=True,
            text=True
        )

        print("STDOUT IS:", result.stdout)
        print("STDERR IS", result.stderr)

        assert os.path.exists(output_file), "Report not generated"
        with open(output_file) as f:
            data = json.load(f)

        expected = {
            "test_pass": "passed",
            "test_fail": "skipped",  # because it's xfail
            "test_skip": "skipped",
        }

        for test_name, expected_status in expected.items():
            actual_status = next((e["status"] for e in data if e["test"] == test_name), None)
            assert actual_status == expected_status, (
                f"{test_name} should be {expected_status}, got {actual_status}"
            )
