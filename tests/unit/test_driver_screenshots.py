import os
from unittest.mock import Mock, patch, call
from pytest_reporter_plus.resolver_driver import resolve_driver, take_screenshot_generic

# ----------------------
# Tests for resolve_driver
# ----------------------

def test_resolve_driver_from_funcargs_priority_order():
    mock_driver = object()
    item = Mock()
    item.funcargs = {"page": mock_driver, "driver": object(), "browser": object()}
    assert resolve_driver(item) is mock_driver

def test_resolve_driver_from_driver_funcarg():
    mock_driver = object()
    item = Mock()
    item.funcargs = {"driver": mock_driver}
    assert resolve_driver(item) is mock_driver

def test_resolve_driver_from_browser_funcarg():
    mock_driver = object()
    item = Mock()
    item.funcargs = {"browser": mock_driver}
    assert resolve_driver(item) is mock_driver

def test_resolve_driver_from_page_for_screenshot():
    mock_driver = object()
    item = Mock()
    item.funcargs = {}
    item.page_for_screenshot = mock_driver
    assert resolve_driver(item) is mock_driver

def test_resolve_driver_fallback_has_screenshot_method():
    mock_driver = Mock()
    mock_driver.screenshot = Mock()
    item = Mock()
    item.funcargs = {"something": mock_driver}
    item.page_for_screenshot = None
    assert resolve_driver(item) is mock_driver

def test_resolve_driver_none_found():
    item = Mock()
    item.funcargs = {"x": object()}
    item.page_for_screenshot = None
    assert resolve_driver(item) is None

# ----------------------
# Tests for take_screenshot_generic
# ----------------------

@patch("os.makedirs")
def test_take_screenshot_with_screenshot_method(mock_makedirs):
    mock_driver = Mock()
    mock_driver.screenshot = Mock()
    item = Mock()
    item.name = "test_case_passes"

    path = take_screenshot_generic("screenshots", item, mock_driver)

    expected_path = "screenshots/test_case_passes_failure.png"
    mock_driver.screenshot.assert_called_once_with(path=expected_path)
    assert path == expected_path
    mock_makedirs.assert_called_once_with("screenshots", exist_ok=True)



@patch("os.makedirs")
def test_take_screenshot_with_save_screenshot_method(mock_makedirs):
    mock_driver = Mock()
    delattr(mock_driver, "screenshot")  # Ensure 'screenshot' is not there
    mock_driver.save_screenshot = Mock()

    item = Mock()
    item.name = "test_case_with_save_screenshot"

    path = take_screenshot_generic("screenshots", item, mock_driver)

    expected_path = "screenshots/test_case_with_save_screenshot_failure.png"
    mock_driver.save_screenshot.assert_called_once_with(expected_path)
    assert path == expected_path


@patch("os.makedirs")
def test_take_screenshot_raises_on_invalid_driver(mock_makedirs):
    mock_driver = object()
    item = Mock()
    item.name = "test_case_fails"

    try:
        take_screenshot_generic("screenshots", item, mock_driver)
    except RuntimeError as e:
        assert "no screenshot method" in str(e)
    else:
        assert False, "Expected RuntimeError was not raised"
