from __future__ import annotations

import json
from pathlib import Path

ISSUES_PATH = Path(__file__).resolve().parents[1] / "issues" / "seed_issues.json"


def escape(text: str) -> str:
    return text.replace('"', '\\"')


def main() -> None:
    issues = json.loads(ISSUES_PATH.read_text(encoding="utf-8"))
    for issue in issues:
        labels = ",".join(issue["labels"])
        body = f"Type: {issue['type']}\\nDifficulty: {issue['difficulty']}\\n\\n{issue['description']}"
        print(
            f'gh issue create --title "{escape(issue["title"])}" '
            f'--body "{escape(body)}" --label "{labels}"'
        )


if __name__ == "__main__":
    main()
