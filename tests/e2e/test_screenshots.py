from unittest.mock import Mock, patch

from pytest_reporter_plus.plugin import take_screenshot_on_failure, take_screenshot_selenium


def test_take_screenshot_on_failure_creates_file():
    item = Mock()
    item.name = "test_fail"
    page = Mock()

    with patch("pytest_reporter_plus.plugin.os.path.join",
               return_value="screenshots/test_fail_failure.png") as mock_join:
        path = take_screenshot_on_failure(item, page)

    page.screenshot.assert_called_once_with(path="screenshots/test_fail_failure.png")
    assert path == "screenshots/test_fail_failure.png"


def test_take_screenshot_selenium_creates_file():
    item = Mock()
    item.name = "test_fail"
    driver = Mock()

    with patch("pytest_reporter_plus.plugin.os.path.join",
               return_value="screenshots/test_fail_failure.png") as mock_join:
        path = take_screenshot_selenium(item, driver)

    driver.save_screenshot.assert_called_once_with("screenshots/test_fail_failure.png")
    assert path == "screenshots/test_fail_failure.png"
