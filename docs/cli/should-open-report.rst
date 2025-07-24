Open HTML Report Automatically (`--should-open-report`)
=======================================================

The `--should-open-report` flag opens the generated HTML report in your system's default web browser after the test run completes. You can control when the report should open using one of three accepted values.

**Default:** ``failed``

Accepted Values
---------------

- ``always`` – Always open the report, regardless of test results.
- ``failed`` – Open the report only if at least one test fails. *(Default)*
- ``never`` – Do not open the report automatically.

How to Use
----------

.. code-block:: bash

   pytest --html-output report_output/index.html --should-open-report always

Use Cases
---------

- ``always`` – Useful during manual test runs or local development to review results immediately.
- ``failed`` – (Default) Ideal for CI/CD environments or when you want to inspect only failed test runs.
- ``never`` – Disable auto-open behavior in headless or automated environments.

Notes
-----

- In headless environments (like CI/CD), the browser might not open even if the flag is set.
- Supported on systems with a default browser configured and GUI access available.