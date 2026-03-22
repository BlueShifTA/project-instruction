from __future__ import annotations

import argparse
import pathlib
import re
import shutil

ROOT = pathlib.Path(__file__).resolve().parents[1]


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9-]+", "-", value.lower()).strip("-")
    slug = re.sub(r"-{2,}", "-", slug)
    return slug


def _package_name(value: str) -> str:
    name = value.lower().replace("-", "_")
    if not re.fullmatch(r"[a-z_][a-z0-9_]*", name):
        raise ValueError(f"Invalid python package name: {value}")
    return name


def _replace_text(path: pathlib.Path, replacements: dict[str, str]) -> None:
    text = path.read_text(encoding="utf-8")
    new_text = text
    for old, new in replacements.items():
        new_text = new_text.replace(old, new)
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        print(f"updated {path.relative_to(ROOT)}")


def _iter_target_files(package_name: str) -> list[pathlib.Path]:
    targets = [
        ROOT / "README.md",
        ROOT / "CLAUDE.md",
        ROOT / "ProjectMap.md",
        ROOT / "pyproject.toml",
        ROOT / "projects/frontend/src/app/layout.tsx",
        ROOT / "projects/frontend/src/app/page.tsx",
        ROOT / "projects/backend/pyproject.toml",
        ROOT / "projects/backend/README.md",
        ROOT / "projects/backend/tests/test_example.py",
        ROOT / "justfile",
    ]
    backend_pkg_dir = ROOT / "projects/backend" / package_name
    if backend_pkg_dir.exists():
        for path in backend_pkg_dir.rglob("*.py"):
            targets.append(path)
    return [path for path in targets if path.exists()]


def main() -> int:
    parser = argparse.ArgumentParser(description="Bootstrap project-template")
    parser.add_argument("--project-name", help="Human-readable project name")
    parser.add_argument("--project-slug", help="kebab-case repo slug")
    parser.add_argument("--python-package", help="backend package name")
    parser.add_argument("--non-interactive", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    project_name = args.project_name or (
        "Project Template"
        if args.non_interactive
        else input("Project name [Project Template]: ").strip() or "Project Template"
    )
    project_slug = args.project_slug or _slugify(project_name)
    package_name = _package_name(args.python_package or project_slug)

    package_dir = ROOT / "projects/backend/package"
    new_package_dir = ROOT / "projects/backend" / package_name
    if package_dir.exists() and new_package_dir != package_dir:
        src_rel = package_dir.relative_to(ROOT)
        dst_rel = new_package_dir.relative_to(ROOT)
        if args.dry_run:
            print(f"would rename {src_rel} -> {dst_rel}")
        else:
            shutil.move(str(package_dir), str(new_package_dir))
            print(f"renamed {src_rel} -> {dst_rel}")

    replacements_common = {
        "Project Template": project_name,
        "project-template": project_slug,
        "Minimal Startup Template": f"{project_name} Template",
        "projects/backend/package": f"projects/backend/{package_name}",
        "package.main:app": f"{package_name}.main:app",
    }
    replacements_backend = {
        "from package.": f"from {package_name}.",
        "import package.": f"import {package_name}.",
        " package.": f" {package_name}.",
        '"package"': f'"{package_name}"',
        "'package'": f"'{package_name}'",
        'name = "package"': f'name = "{package_name}"',
    }

    if not args.dry_run:
        for path in _iter_target_files(package_name):
            replacements = dict(replacements_common)
            if "projects/backend/" in str(path):
                replacements.update(replacements_backend)
            _replace_text(path, replacements)
    else:
        for path in _iter_target_files(package_name):
            print(f"would update {path.relative_to(ROOT)}")

    print("\nNext steps:")
    print("1. just install")
    print("2. just run-backend")
    print("3. just run-frontend")
    print("4. just test && just lint")
    print("5. after first successful build, run: just template-clean")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
