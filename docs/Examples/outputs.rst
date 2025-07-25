Comprehensive Output Capture
============================

`pytest-html-plus` ensures that all test-related output is automatically captured and embedded in the HTML report — making debugging easier and richer than ever.

What gets captured:
-------------------

- **Standard Output (`print()` statements):** Console logs from your test functions or libraries are displayed clearly.
- **Logging Output (`logging` module):** All logs from any configured logger are preserved and shown in the test detail view.
- **Screenshots:** If you're using tools like Selenium or Playwright and attach screenshots to the test's `request.node`, they will be displayed directly in the test report.

.. tip::
   There's no additional setup required. If your test emits output or attaches media, it’ll be available in the report automatically.

User Experience:
----------------

- Output is shown inside the expandable **"Captured Output"** section within each test's detail.
- Screenshots and media appear in a **"Media"** section for better visual traceability.
- Each captured item — including logs and printed output — comes with a **copy button** for quick sharing or further analysis.

This allows your team to analyze failures without digging through logs or rerunning tests just to reproduce console output or visual states.
