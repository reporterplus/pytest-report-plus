from collections import Counter

# def main():
#     # detect_flakes()
#     generate_flaky_html("flake_data/flake_report.json", "flake_data/flake_report.html")

def generate_flaky_html(flake_summary: dict, output_html_path):
    rows_html = ""
    if not flake_summary:
        rows_html = """
            <tr>
                <td colspan="5" style="text-align: center; padding: 1em;">
                    🎉 No flaky tests detected in this run.
                </td>
            </tr>
        """
    else:
        for test_name, test_data in flake_summary.items():
            status_list = test_data["statuses"]
            total_runs = len(status_list)
            status_count = Counter(status_list)
            majority_status = status_count.most_common(1)[0][1]
            last_failed = test_data["last_failed"]
            flakiness_pct = round((total_runs - majority_status) / total_runs * 100, 2)

            row = f"""
            <tr>
                <td>{test_name}</td>
                <td>{total_runs}</td>
                <td>{dict(status_count)}</td>
                <td class="{'flaky' if flakiness_pct > 0 else ''}">{flakiness_pct}%</td>
                <td>{last_failed}</td>
            </tr>
            """
            rows_html += row

    with open(output_html_path, "w") as f:
        f.write(FLAKY_HTML_TEMPLATE.replace("{{ rows }}", rows_html))


# Define the HTML template as a global string or in a separate file
FLAKY_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Flaky Test Report</title>

    <style>
        body { font-family: Arial, sans-serif; background: #f7f9fc; padding: 2em; }
        h1 { color: #333; }
        table { width: 100%; border-collapse: collapse; margin-top: 2em; background: white; }
        th, td { padding: 0.75em; border: 1px solid #ccc; text-align: left; }
        th { background-color: #eee; }
        tr:nth-child(even) { background-color: #f9f9f9; }
        .flaky { color: red; font-weight: bold; }
    </style>
</head>
<body>
    <h1>🌀 Flaky Test Summary</h1>
    <table>
        <thead>
            <tr>
                <th>Test Name</th>
                <th>Total Runs</th>
                <th>Status Count</th>
                <th>Flakiness %</th>
                <th>Last Failed</th>
            </tr>
        </thead>
        <tbody>
            {{ rows }}
        </tbody>
    </table>
    <script>
    function calculateFlakiness(statuses) {
  const total = statuses.length;
  const statusCount = statuses.reduce((acc, status) => {
    acc[status] = (acc[status] || 0) + 1;
    return acc;
  }, {});
  // Majority status count
  const majorityCount = Math.max(...Object.values(statusCount));
  return ((total - majorityCount) / total * 100).toFixed(2);
}

function renderTable(data, sortBy) {
  const tbody = document.querySelector("#flakeTable tbody");
  tbody.innerHTML = "";

  // Convert object to array for sorting
  const rows = Object.entries(data).map(([testName, info]) => {
    return {
      testName,
      flakiness: parseFloat(calculateFlakiness(info.statuses)),
      lastFailed: new Date(info.last_failed)
    };
  });

  if (sortBy === "flakiness") {
    rows.sort((a, b) => b.flakiness - a.flakiness);
  } else if (sortBy === "recent") {
    rows.sort((a, b) => b.lastFailed - a.lastFailed);
  }

  for (const row of rows) {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${row.testName}</td>
      <td>${row.flakiness}%</td>
      <td>${row.lastFailed.toLocaleString()}</td>
    `;
    tbody.appendChild(tr);
  }
}

document.getElementById("sortSelect").addEventListener("change", (e) => {
  renderTable(flakeData, e.target.value);
});

// Initial render
renderTable(flakeData, "flakiness");
</script>

</body>
</html>"""




#
# if __name__ == "__main__":
#     main()