# 🧪 pytest-reporter-plus

A powerful, plug-and-play Pytest plugin to generate **HTML + JSON reports**, detect **flaky tests**, and optionally **send reports via email**. Works beautifully with or without `xdist`.

---

## ✨ Features

🧩 Unified Test Reports: Get a single, easy-to-read HTML report summarizing all your test results — no hassle, just clarity.

🔄 Flaky Test Detection: Automatically flags flaky tests so you can spot and fix inconsistent failures quickly.

📸 Screenshot Support: View screenshots directly in the report to understand failures faster.

📧 Email Test Reports: Send your reports via email effortlessly using SendGrid integration.

🐢 Spot Slow Tests: Highlights the slowest tests so you know where to optimize your suite.

⏱️ Sort & Filter: Easily sort tests by duration or filter by custom tags and skip status to focus on what matters.

---

## 🚀 Installation

```bash
pip install pytest-reporter-plus
# or with Poetry
poetry add --dev pytest-reporter-plus
```


## 🧾 Usage
Generate HTML + JSON reports:

```bash
pytest --html-report --json-report
```
You’ll get:

report.html – a clean, styled HTML report

playwright_report.json – structured data for integrations

You can also choose to custom name your output HTML report by mentioning the name of the html report

## 🔁 Flaky Test Detection
If a test is retried multiple times (e.g. due to a --reruns plugin), the report will flag it as FLAKY.

In the HTML report, you’ll see a badge like:

// Add  snapshot here

## 📧 Email Report (Optional)
Send the HTML report via email using --send-email.

### Setup Environment Variables
Create an emailenv file in your project folder that has the following

```commandline
sender_email=you@example.com
recipient_email=team@example.com
report_path=report.html
subject=Your Test Report
smtp_server=smtp.sendgrid.net
smtp_port=587
email_password=your_sendgrid_api_key

```

## Run
```commandline
pytest --html-report --send-email
```

## 🤝 Contributions
PRs, issues, and feature requests are welcome! Let's make this tool more awesome together.

## 📛 Naming
Why pytest-reporter-plus?

Because it does more than just reporting – it’s your enhanced test summary companion ✨


## 📜 License

MIT