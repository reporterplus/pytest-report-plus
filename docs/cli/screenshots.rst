Capture Screenshots (`--capture-screenshots`)
=============================================

The `--capture-screenshots` flag controls when screenshots are taken during test execution. This is especially valuable in UI automation to debug failures or detect flaky behavior.

Overview
--------

- **Default**: `failed`
- **Allowed Values**: `always`, `failed`, `never`
- **Usage Context**: UI tests, flaky test debugging, visual regression

Example
-------

.. code-block:: bash

   pytest --capture-screenshots=always

This will capture screenshots for all test cases, regardless of result.

Use Cases
---------

- **Flaky UI Tests**: Capturing screenshots only on failure (`failed`) is helpful to understand intermittent issues.
- **Debugging**: Use `always` when actively debugging tests to see step-by-step screenshots.(Experimental)
- **CI Pipelines**: Set to `failed` to save space and avoid clutter unless a test fails.
- **Local Runs**: You may choose `always` during development, but `failed` in CI.

Screenshot Storage
------------------

- Screenshots are saved in the `report_output/screenshots/` directory by default.
- Filenames are automatically derived from the test node ID and status.

Integration
-----------

- Works well with `--html-output`, which embeds screenshot thumbnails in the HTML report.
- Captured screenshots are also referenced in the JSON report.

.. note::

   To avoid unnecessary storage usage, use `--capture-screenshots=failed` in CI environments.
