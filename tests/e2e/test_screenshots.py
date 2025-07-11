from unittest.mock import Mock, patch
from pytest_reporter_plus.plugin import take_screenshot_generic


# @patch("pytest_reporter_plus.plugin.os.makedirs")
# @patch("pytest_reporter_plus.plugin.os.path.join", return_value="custom_dir/custom_file.png")
# def test_take_screenshot_with_custom_path(mock_join, mock_makedirs):
#     mock_driver = Mock()
#     mock_driver.screenshot = Mock()
#
#     item = Mock()
#     item.name = "custom_test"
#
#     path = take_screenshot_generic("custom_dir", item, mock_driver)
#
#     mock_makedirs.assert_called_once_with("custom_dir", exist_ok=True)
#     mock_join.assert_called_once_with("custom_dir", "custom_test_failure.png")
#     mock_driver.screenshot.assert_called_once_with(path="custom_dir/custom_file.png")
#     assert path == "custom_dir/custom_file.png"

