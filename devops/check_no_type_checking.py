"""Ban 'if TYPE_CHECKING:' import blocks.

TYPE_CHECKING guards hide circular import cycles rather than fixing them.
Move shared types to a leaf module that both sides import unconditionally.

See instruction/reference/PYTHON_STYLE.md for the full rationale.
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
                stripped = line.strip()
                if stripped == "if TYPE_CHECKING:" or stripped.startswith("if TYPE_CHECKING:"):
                    violations.append(f"{path.relative_to(ROOT)}:{lineno}")

    if violations:
        print("ERROR: 'if TYPE_CHECKING:' blocks are banned.")
        print("Move shared types to a leaf module both sides import unconditionally.")
        print("See instruction/reference/PYTHON_STYLE.md for rationale.")
        print("Violations:")
        for v in violations:
            print(f"  {v}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
