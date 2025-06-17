# Contributing to pytest-reporter-plus and/or pytest-report-plus

Thank you for thinking about contributing to this project! Whether you're fixing a bug, improving the documentation, or proposing a new feature — you're welcome here.

### 📁 Project Setup

Fork and Clone
```
git clone https://github.com/reach2jeyan/pytest-report-plus.git
cd pytest-report-plus
Install Dependencies
```

```
docker build -t pytest-reporter-plus . 
```

### Run Tests

pytest

✅ Before Sending a Pull Request
 - All tests pass locally.

 - New features include test coverage.

 - Code is formatted using black, and imports are sorted with isort.

 - Docstrings or README are updated where needed.

 - PR focuses on a single, clear purpose.

💡 What Can You Contribute?

🐛 Bug fixes — Fix something broken or improve test stability.

📈 New features — Keep it lean; prefer practical and minimalistic additions.

🧹 Refactoring — Improve readability, structure, or performance without changing behavior.

📝 Docs — Even typo corrections are appreciated!

🧪 Code Style

Follow PEP8.

Use black and isort:
```
black .
isort .
```

### 🧰 Plugin Philosophy

- Keep it lightweight — no extra assets, charts, or JS-heavy dashboards.

- Require zero config — should work out-of-the-box.

- Respect pytest idioms — no custom test decorations, stick to pytest.mark.

### 💬 Communication & Etiquette

- Be respectful, helpful, and open to discussion.

- Ask before working on major changes — open an issue or discussion first.

- Review others’ contributions kindly.

### 📜 License
By contributing, you agree your code will be licensed under the same license as this repo (MIT or your chosen license).

