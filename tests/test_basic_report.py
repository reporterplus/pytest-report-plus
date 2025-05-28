import pytest
import os
import json

def test_basic_report_generation(tmp_path):
    test_file = tmp_path / "sample_test.py"
    import textwrap

    test_file.write_text(textwrap.dedent("""
        def test_example():
            print("hello world")
            assert True
    """))

    result = pytest.main([
        str(test_file),
        "--json-report", str(tmp_path / "out.json")
    ])

    assert result == 0
    assert (tmp_path / "out.json").exists()

    with open(tmp_path / "out.json") as f:
        data = json.load(f)
        assert any("hello world" in t.get("stdout", "") for t in data)
