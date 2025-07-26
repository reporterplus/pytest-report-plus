from pytest_html_plus.utils import extract_error_block

def test_error_block_basic():
    error = "line 1\nE AssertionError: something went wrong\nline 3\nE ValueError: another error"
    expected = "E AssertionError: something went wrong\nE ValueError: another error"
    assert extract_error_block(error) == expected

def test_error_block_spaces_and_blank_lines():
    error = "\n\n   E TypeError\n\n   \nE IndexError\n"
    expected = "E TypeError\nE IndexError"
    assert extract_error_block(error) == expected

def test_error_block_no_E_lines():
    error = "line 1\nline 2"
    expected = "line 1\nline 2"
    assert extract_error_block(error) == expected  # fallback logic

def test_error_block_empty():
    assert extract_error_block("") == ""

def test_error_block_none():
    assert extract_error_block(None) == ""
