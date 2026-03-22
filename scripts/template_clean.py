from __future__ import annotations

import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]


def main() -> int:
    marker = ROOT / ".template-cleaned"
    marker.write_text(
        "Template cleanup completed. Remove example routes/components/tests not needed.\n",
        encoding="utf-8",
    )
    print("Template cleanup marker written: .template-cleaned")
    print("Manual follow-up:")
    print("- Remove or replace example backend route: /api/example/echo")
    print("- Remove or replace starter frontend landing page content")
    print("- Update CLAUDE.md and ProjectMap.md for your real project")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
