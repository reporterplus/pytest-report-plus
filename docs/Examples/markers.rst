Tagging and Filtering Tests
===========================

`pytest-html-plus` respects all `@pytest.mark.*` markers.

Use tags like:

- `@pytest.mark.api`
- `@pytest.mark.smoke`
- `@pytest.mark.critical`
- etc.

These markers will be **visible in the HTML UI** and can be used to filter test cases visually.

The HTML report dynamically shows **all used markers as clickable filters**, along with a **count of test cases** associated with each tag. This makes it easy to:

- Slice test results by test type or priority
- Quickly find failing critical or smoke tests
- Understand distribution of tests across various categories

.. tip::
   You don't need to register markers in `pytest.ini` unless you want to enforce or document them.
