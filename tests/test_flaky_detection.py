import json

import pytest


def test_flaky_detection(tmp_path):
    import textwrap
    test_file = tmp_path / "flaky_test.py"
    test_file.write_text(textwrap.dedent("""
        import itertools
        counter = itertools.count()
        def test_flaky():
            assert next(counter) > 0
    """))

    result_code = pytest.main([
        str(test_file),
        "--reruns=2",
        "--json-report", str(tmp_path / "out.json")
    ])
    assert result_code == 0

    with open(tmp_path / "out.json") as f:
        data = json.load(f)
        flaky_tests = [t for t in data if t.get("flaky")]
        assert flaky_tests, "Expected at least one flaky test"
