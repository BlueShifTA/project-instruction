"""Ban 'from __future__ import annotations' in Python 3.13+ code.

Python 3.13 is the project baseline. Modern union syntax (list[str] | None,
X | None) works natively. The future import is unnecessary and banned.
"""

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

SEARCH_DIRS = [
    ROOT / "projects",
    ROOT / "devops",
]

EXCLUDE_DIRS = {".venv", "__pycache__", "node_modules", ".git"}


def main() -> int:
    violations: list[str] = []
    for search_dir in SEARCH_DIRS:
        for path in search_dir.rglob("*.py"):
            if any(part in EXCLUDE_DIRS for part in path.parts):
                continue
            for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if line.strip() == "from __future__ import annotations":
                    violations.append(f"{path.relative_to(ROOT)}:{lineno}")

    if violations:
        print("ERROR: 'from __future__ import annotations' is banned (Python 3.13+ baseline).")
        print("Remove it and use native syntax: list[str] | None, X | None.")
        print("Violations:")
        for v in violations:
            print(f"  {v}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
