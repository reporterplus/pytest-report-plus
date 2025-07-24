Tagging and Filtering Tests
===========================

pytest-html-plus respects all `@pytest.mark.*` markers.

Use tags like `@pytest.mark.api`, `@pytest.mark.smoke`, `@pytest.mark.critical`, etc.

These markers will be visible in the HTML UI and can be filtered visually.

.. tip::
   You don't need to register markers in `pytest.ini` unless you want to enforce them.
