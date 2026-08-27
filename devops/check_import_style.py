"""Enforce the module-import rule: import modules, never their members.

Banned:
- ``from fastapi import APIRouter``            -> ``import fastapi``
- ``from typing import Annotated``             -> ``import typing``
- ``from package.domain.models import Thing``  -> ``import package.domain.models as pdm``
- ``from ..domain.models import Thing``        -> parent-relative imports are never allowed

Allowed:
- ``import asyncio`` / ``import fastapi`` / ``import package.domain.models as pdm``
- ``from .example import router`` -- the same-directory exception

Same-directory imports that pull in a *class* must come from a private module
(``from ._models import Thing``): the class is the public surface, the file that
happens to hold it is not.

See instruction/reference/PYTHON_STYLE.md for the full rationale.
"""

import argparse
import ast
import dataclasses
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCAN_ROOTS = ("projects", "devops", "docs")
SKIP_DIRS = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".next",
}


@dataclasses.dataclass(frozen=True)
class Violation:
    path: pathlib.Path
    line: int
    message: str

    def format(self) -> str:
        return f"{self.path}:{self.line}: {self.message}"


def _iter_python_files(root: pathlib.Path) -> list[pathlib.Path]:
    search_dirs = [root / name for name in SCAN_ROOTS] if root == ROOT else [root]
    files: list[pathlib.Path] = []
    for search_dir in search_dirs:
        if not search_dir.exists():
            continue
        for path in search_dir.rglob("*.py"):
            if any(part in SKIP_DIRS for part in path.parts):
                continue
            files.append(path)
    return sorted(files)


def _sibling_module(path: pathlib.Path, module: str) -> pathlib.Path | None:
    """Resolve ``from .module import ...`` to the file it refers to."""
    candidates = [
        path.parent / f"{module}.py",
        path.parent / module / "__init__.py",
    ]
    return next((c for c in candidates if c.is_file()), None)


def _classes_defined_in(path: pathlib.Path) -> set[str]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except OSError, UnicodeDecodeError, SyntaxError:
        return set()
    return {node.name for node in tree.body if isinstance(node, ast.ClassDef)}


def _check_relative_import(
    node: ast.ImportFrom, path: pathlib.Path, rel: pathlib.Path
) -> list[Violation]:
    """Same-directory import: allowed, unless it is a wildcard or an unprivate class."""
    imported = [alias.name for alias in node.names]
    if "*" in imported:
        return [Violation(rel, node.lineno, "wildcard imports are banned; name each symbol")]

    module = node.module
    if module is None or module.startswith("_"):
        return []

    target = _sibling_module(path, module)
    if target is None:
        return []

    classes = _classes_defined_in(target).intersection(imported)
    if not classes:
        return []

    names = ", ".join(sorted(classes))
    return [
        Violation(
            rel,
            node.lineno,
            f"class import from a public module: rename '{module}.py' to '_{module}.py' "
            f"and import as 'from _{module} import {names}'. "
            "The class is the public surface, not the file holding it.",
        )
    ]


def _find_violations(path: pathlib.Path, rel: pathlib.Path) -> list[Violation]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(rel))
    except (UnicodeDecodeError, SyntaxError) as exc:
        return [Violation(rel, 1, f"failed to parse: {exc}")]

    violations: list[Violation] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.ImportFrom):
            continue
        if node.level >= 2:
            violations.append(
                Violation(
                    rel,
                    node.lineno,
                    "parent-relative import ('from ..'): import the module absolutely instead",
                )
            )
        elif node.level == 1:
            violations.extend(_check_relative_import(node, path, rel))
        else:
            source = node.module or "?"
            violations.append(
                Violation(
                    rel,
                    node.lineno,
                    f"member import from '{source}': import the module instead "
                    f"('import {source}' / 'import {source} as alias') and access via its namespace",
                )
            )
    return violations


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "root",
        nargs="?",
        type=pathlib.Path,
        default=ROOT,
        help="directory to scan (defaults to the repository roots)",
    )
    args = parser.parse_args()
    root = args.root.resolve()

    violations: list[Violation] = []
    for path in _iter_python_files(root):
        violations.extend(_find_violations(path, path.relative_to(root)))

    if not violations:
        return 0

    print("check_import_style: import the module, never its members.")
    print("See instruction/reference/PYTHON_STYLE.md for rationale.")
    for violation in sorted(violations, key=lambda v: (str(v.path), v.line)):
        print(f"  {violation.format()}")
    print(f"\n{len(violations)} violation(s) found.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
