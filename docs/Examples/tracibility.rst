External Link Markers
=====================

You can attach **external links** (such as JIRA issues, test case IDs, or bug reports) directly to your test functions using standard ``pytest.mark`` decorators.

These links will be **automatically extracted** and displayed in the generated HTML report, making it easier to navigate to external systems right from the test results.

Supported Marker Names
----------------------

The following marker names are supported:

- ``@pytest.mark.link``
- ``@pytest.mark.testcase``
- ``@pytest.mark.jira``
- ``@pytest.mark.issue``
- ``@pytest.mark.ticket``

Example
-------

.. code-block:: python

    import pytest

    @pytest.mark.jira("https://jira.example.com/browse/PROJ-123")
    @pytest.mark.testcase("https://testcases.example.com/case/5678")
    def test_login():
        assert True

These links will appear in the report next to the test case, allowing testers and developers to quickly navigate to the relevant external resources.

How It Works
------------

The plugin extracts all markers with the supported names from each test item and the extracted links are then rendered in the HTML report automatically.

.. tip::
    1. Searching for a quoted ID(For eg: Jira id/ ticket id/ notion id / test case id etc..) in the report’s search bar will show you a list of all test cases associated with that ID. This makes it easier to trace test automation coverage during release or group test results by external references.
    2. You can also use the **Show Untracked** filter in the report to list only those test cases that do **not** contain any of the supported external link markers. This helps in identifying test cases that aren't yet linked to any tracking or documentation system.