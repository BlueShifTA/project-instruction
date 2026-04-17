import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]


def main() -> int:
    marker = ROOT / ".template-cleaned"
    marker.write_text(
        "Template cleanup completed. Remove example routes/components/tests not needed.\n",
        encoding="utf-8",
    )
    print("Template cleanup marker written: .template-cleaned")
    print("")
    print("Dev laptop check:")
    print("  rtk --version && rtk gain   # RTK must be active for token savings")
    print("")
    print("Manual follow-up:")
    print("- Remove or replace example backend route: /api/example/echo")
    print("- Remove or replace starter frontend landing page content")
    print("- Update CLAUDE.md and ProjectMap.md for your real project")
    print("  Regenerate: just project-map")
    print("- After any backend API change, regenerate frontend types:")
    print("  just run-backend  (in one terminal)")
    print("  just generate-frontend-types  (in another)")
    print("- Replace or delete instruction/profiles/surapat/ with your own profile")
    print("  (it's an example — keep the structure, swap the content)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
