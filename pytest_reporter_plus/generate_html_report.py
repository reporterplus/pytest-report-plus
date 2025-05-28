import argparse
import json
import os
import shutil
from datetime import datetime


def main():
    parser = argparse.ArgumentParser(description="Generate HTML report from Playwright JSON report")
    parser.add_argument("--report", required=True, help="Path to the JSON report file")
    parser.add_argument("--screenshots", default="screenshots", help="Folder path where screenshots are saved")
    parser.add_argument("--output", default="report_output", help="Output folder for HTML report")
    args = parser.parse_args()

    reporter = JSONReporter(
        report_path=args.report,
        screenshots_dir=args.screenshots,
        output_dir=args.output,
    )
    reporter.load_report()
    reporter.generate_html_report()


class JSONReporter:
    def __init__(self, report_path="playwright_report.json", screenshots_dir="screenshots", output_dir="report_output"):
        self.parsed_data = None
        self.report_path = report_path
        self.screenshots_dir = screenshots_dir
        self.output_dir = output_dir
        self.results = []
        all_markers = set()
        for test in self.results:
            for marker in test.get("markers", []):
                all_markers.add(marker)
        all_markers = sorted(all_markers)

    def load_report(self):
        with open(self.report_path) as f:
            self.results = json.load(f)

    def log_result(
            self,
            test_name,
            nodeid,
            status,
            duration,
            error=None,
            markers=None,
            filepath=None,
            lineno=None,
            stdout=None,
            stderr=None,
            screenshot=None,
            logs=None,
            worker=None
    ):
        result = {
            "test": test_name,
            "nodeid": nodeid,
            "status": status,
            "duration": duration,
            "error": error,
            "markers": markers or [],
            "file": filepath,
            "line": lineno,
            "stdout": stdout,
            "stderr": stderr,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "screenshot": screenshot,
            "logs": logs or [],
            "worker": worker
        }
        if error:
            result["error"] = error
        self.results.append(result)

    def write_report(self):
        dir_path = os.path.dirname(os.path.abspath(self.report_path))

        # Ensure directory exists
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)

        try:
            with open(self.report_path, "w", encoding="utf-8") as f:
                json.dump(self.results, f, indent=2)
            print(f"✅ JSON report successfully written to {self.report_path}")
        except Exception as e:
            print(f"❌ Failed to write JSON report to {self.report_path}: {e}")

    def copy_all_screenshots(self):
        screenshots_output_dir = os.path.join(self.output_dir, "screenshots")
        os.makedirs(screenshots_output_dir, exist_ok=True)

        print(f"📦 Copying all .png files from '{self.screenshots_dir}' to '{screenshots_output_dir}'")

        for root, _, files in os.walk(self.screenshots_dir):
            for file in files:
                if file.endswith(".png"):
                    src_path = os.path.join(root, file)
                    dest_path = os.path.join(screenshots_output_dir, file)
                    if not os.path.exists(dest_path):
                        shutil.copyfile(src_path, dest_path)
                        print(f"✅ Copied: {src_path} → {dest_path}")

    def find_screenshot_and_copy(self, test_name):
        screenshots_output_dir = os.path.join(self.output_dir, "screenshots")
        os.makedirs(screenshots_output_dir, exist_ok=True)

        # We'll look for any .png file where test_name is contained in the filename (partial match)
        for root, _, files in os.walk(self.screenshots_dir):
            for file in files:
                if file.endswith(".png") and test_name in file:
                    src_path = os.path.join(root, file)

                    # Name destination file exactly as the source (or you can rename if needed)
                    dest_path = os.path.join(screenshots_output_dir, file)

                    shutil.copyfile(src_path, dest_path)

                    # Return relative path from output_dir for HTML src
                    return os.path.join("screenshots", file)
        return None

    def generate_html_report(self):
        # Extract all unique markers
        all_markers = set()
        for test in self.results:
            for marker in test.get("markers", []):
                all_markers.add(marker)

        html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8" />
    <title>Playwright Test Report</title>
    <a href="flake_report.html" target="_blank">🌀 View Flaky Test Summary</a>
    <style>
      body {{ font-family: Arial, sans-serif; padding: 1rem; background: #f9f9f9; }}
      .test {{ border: 1px solid #ddd; margin-bottom: 0.5rem; border-radius: 5px; background: white; }}
      .header {{ padding: 0.5rem; cursor: pointer; display: flex; justify-content: space-between; align-items: center; }}
      .header.passed {{ background: #e6f4ea; color: #2f7a33; }}
      .header.failed {{ background: #fdecea; color: #a83232; }}
      .header.skipped {{  background: #fff8e1; color: #b36b00;  }}
       .header.error {{  background: #f0f0f0; color: #f0f0f0;  }}
      .details {{ padding: 0.5rem 1rem; display: none; border-top: 1px solid #ddd; }}
      .toggle::before {{ content: "▶"; display: inline-block; margin-right: 0.5rem; transition: transform 0.3s ease; }}
      .header.expanded .toggle::before {{ transform: rotate(90deg); }}
      img {{ max-width: 100%; margin-top: 0.5rem; border: 1px solid #ccc; border-radius: 3px; }}
      .checkbox-container {{ margin-bottom: 1rem; }}
    </style>
    <script>
      function toggleDetails(headerElem) {{
        headerElem.classList.toggle('expanded');
        const details = headerElem.nextElementSibling;
        details.style.display = (details.style.display === 'block') ? 'none' : 'block';
      }}

      function toggleFilter(longestCheckbox) {{
        const failedCheckbox = document.getElementById('failedOnlyCheckbox');
        const testsContainer = document.getElementById('tests-container');
        const testElements = Array.from(testsContainer.querySelectorAll('.test'));

        if (longestCheckbox.checked) {{
          failedCheckbox.checked = false;
          testElements.forEach(el => el.style.display = 'block');
          testElements.sort((a, b) => {{
            const aDuration = parseFloat(a.querySelector('.timestamp').textContent.replace(/[^\d.]/g, '')) || 0;
            const bDuration = parseFloat(b.querySelector('.timestamp').textContent.replace(/[^\d.]/g, '')) || 0;
            return bDuration - aDuration;
          }});
          testElements.forEach(el => testsContainer.appendChild(el));
        }} else {{
          testElements.forEach(el => el.style.display = 'block');
        }}
        filterByMarkers(); // Reapply marker filter
      }}

      function toggleFailedOnly(failedCheckbox) {{
        const longestCheckbox = document.getElementById('longestOnlyCheckbox');
        const testElements = document.querySelectorAll('.test');
        if (failedCheckbox.checked) {{
          longestCheckbox.checked = false;
          testElements.forEach(el => {{
            const header = el.querySelector('.header');
            const isFailed = header.classList.contains('failed');
            el.style.display = isFailed ? 'block' : 'none';
          }});
        }} else {{
          testElements.forEach(el => el.style.display = 'block');
        }}
        filterByMarkers(); // Reapply marker filter
      }}

      function filterByMarkers() {{
  const selected = Array.from(document.querySelectorAll('.marker-filter input[type="checkbox"]:checked')).map(cb => cb.value);
  const failedOnly = document.getElementById('failedOnlyCheckbox').checked;
  document.querySelectorAll('.test').forEach(el => {{
    const markers = el.getAttribute('data-markers').split(',');
    const isFailed = el.querySelector('.header').classList.contains('failed');
    const showAllMarkers = selected.length === 0;
    const matchesMarker = showAllMarkers || selected.some(m => markers.includes(m));
    const matchesFailed = !failedOnly || isFailed;
    el.style.display = (matchesMarker && matchesFailed) ? 'block' : 'none';
  }});
}}


      window.onload = function() {{
        const failedCheckbox = document.getElementById('failedOnlyCheckbox');
        const longestCheckbox = document.getElementById('longestOnlyCheckbox');
        failedCheckbox.checked = true;
        toggleFailedOnly(failedCheckbox);
        failedCheckbox.addEventListener('change', () => toggleFailedOnly(failedCheckbox));
        longestCheckbox.addEventListener('change', () => toggleFilter(longestCheckbox));

        const markerCheckboxes = document.querySelectorAll('.marker-filter input[type="checkbox"]');
        markerCheckboxes.forEach(cb => cb.addEventListener('change', filterByMarkers));
      }};
    </script>
    </head>
    <body>
    <div class="checkbox-container">
      <label>
        <input type="checkbox" id="failedOnlyCheckbox" />
        Show only failed tests
      </label>
      <label style="margin-left: 1rem;">
        <input type="checkbox" id="longestOnlyCheckbox" />
        Sort by longest running tests
      </label>
    </div>

    <div id="markersFilter" class="marker-filter" style="margin-bottom: 1rem;">
      <strong>Filter by Markers:</strong><br/>
    """

        # Add checkboxes for all markers
        for marker in sorted(all_markers):
            html += f'<label><input type="checkbox" value="{marker}" /> {marker}</label> '

        html += '<div id="tests-container">'

        # Generate test blocks
        for test in self.results:
            status_class = (
                'passed' if test['status'] == 'passed' else
                'failed' if test['status'] == 'failed' else
                'skipped'
            )
            error_html = f"<pre>{test.get('error', '')}</pre>" if test.get('error') else ""
            screenshot_path = self.find_screenshot_and_copy(test['test'])
            screenshot_html = f'<img src="{screenshot_path}" alt="Screenshot">' if screenshot_path else ""
            marker_str = ",".join(test.get("markers", []))
            stdout_html = ""
            if test.get('stdout'):
                stdout_html = f"<div><strong>STDOUT:</strong><pre>{test['stdout']}</pre></div>"

            stderr_html = ""
            if test.get('stderr'):
                stderr_html = f"<div><strong>STDERR:</strong><pre>{test['stderr']}</pre></div>"

            logs_html = ""
            if test.get('logs'):
                logs_html = f"<div><strong>Logs:</strong><pre>{test['logs']}</pre></div>"

            flaky_badge = ""
            if test.get("flaky"):
                flaky_badge = (
                    '<span class="is-flaky" '
                    'style="background:#f39c12;color:white;padding:2px 6px;'
                    'border-radius:3px;font-weight:bold;font-size:0.85em;">FLAKY</span>'
                )

            html += f'''
            

      <div class="test" data-markers="{marker_str}">
        <div class="header {status_class}" onclick="toggleDetails(this)">
          <span class="toggle"></span>
          <span><strong>{test["test"]}</strong> — {test["status"].upper()}</span>
          <span class="worker-id" style="background: #ddd; border-radius: 3px; padding: 2px 5px; font-size: 0.85em; font-weight: bold;">{test["worker"]}</span>
          <span class="worker-id" style="background: #ddd; border-radius: 3px; padding: 2px 5px; font-size: 0.85em; font-weight: bold;">{flaky_badge}</span>
          <span class="timestamp">⏱ {test.get("duration", 0):.2f}s</span>
        </div>
        <div class="details">
          {error_html}
          {screenshot_html}
          {stdout_html}
        {stderr_html}
        {logs_html}
        </div>
      </div>
    '''

        # Add summary
        total_tests = len(self.results)
        failed_tests = sum(1 for t in self.results if t['status'] == 'failed')
        error_tests = sum(1 for t in self.results if t['status'] == 'error')
        slowest_test = max(self.results, key=lambda x: x.get('duration', 0), default=None)
        slowest_test_name = slowest_test['test'] if slowest_test else 'N/A'
        slowest_test_duration = slowest_test.get('duration', 0) if slowest_test else 0

        summary_html = f"""
            <div style="padding: 1rem; background: {'#e6f4ea' if failed_tests == 0 and error_tests == 0 else '#fdecea'}; 
            border: 1px solid {'#2f7a33' if failed_tests == 0 and error_tests == 0 else '#a83232'}; 
            border-radius: 5px; margin-bottom: 1rem;">
              {'<strong>Bingo!</strong> All your tests passed!' if failed_tests == 0 and error_tests == 0 else
        f'Total tests: {total_tests}, Failures: {failed_tests}, Errors: {error_tests}.'}
              The slowest test was <strong>{slowest_test_name}</strong> at {slowest_test_duration:.2f}s.
            </div>
            """

        html = html.replace('<div id="tests-container">', summary_html + '<div id="tests-container">')
        html += "</div></body></html>"

        # Save report
        os.makedirs(self.output_dir, exist_ok=True)
        output_file = os.path.join(self.output_dir, "report.html")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html)

if __name__ == "__main__":
    main()
