"""Functional tests for the import-style checker.

The checker is a CLI, so every test invokes it as a subprocess against a
throwaway tree and asserts on exit code plus the reported file:line list.
"""

import pathlib
import subprocess
import sys

CHECKER = pathlib.Path(__file__).resolve().parent / "check_import_style.py"


def _run(root: pathlib.Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CHECKER), str(root)],
        capture_output=True,
        text=True,
        check=False,
    )


def _write(root: pathlib.Path, relative: str, source: str) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(source, encoding="utf-8")


def test_third_party_member_import_is_rejected(tmp_path: pathlib.Path) -> None:
    _write(tmp_path, "app.py", "from fastapi import APIRouter\n")

    result = _run(tmp_path)

    assert result.returncode == 1
    assert "app.py:1" in result.stdout


def test_stdlib_member_import_is_rejected(tmp_path: pathlib.Path) -> None:
    _write(tmp_path, "app.py", "from typing import Annotated\n")

    result = _run(tmp_path)

    assert result.returncode == 1
    assert "app.py:1" in result.stdout


def test_own_package_member_import_is_rejected(tmp_path: pathlib.Path) -> None:
    _write(tmp_path, "app.py", "from package.domain.models import Thing\n")

    result = _run(tmp_path)

    assert result.returncode == 1
    assert "app.py:1" in result.stdout


def test_parent_relative_import_is_rejected(tmp_path: pathlib.Path) -> None:
    _write(tmp_path, "pkg/api/routes.py", "from ..domain.models import Thing\n")

    result = _run(tmp_path)

    assert result.returncode == 1
    assert "routes.py:1" in result.stdout


def test_module_imports_are_accepted(tmp_path: pathlib.Path) -> None:
    _write(
        tmp_path,
        "app.py",
        "import asyncio\nimport fastapi\nimport package.domain.models as pdm\nimport pandas as pd\n",
    )

    result = _run(tmp_path)

    assert result.returncode == 0, result.stdout


def test_same_directory_relative_import_is_accepted(tmp_path: pathlib.Path) -> None:
    _write(tmp_path, "pkg/example.py", "router = 1\n")
    _write(tmp_path, "pkg/__init__.py", "from .example import router\n")

    result = _run(tmp_path)

    assert result.returncode == 0, result.stdout


def test_same_directory_class_import_needs_private_module(tmp_path: pathlib.Path) -> None:
    _write(tmp_path, "pkg/models.py", "class Thing:\n    pass\n")
    _write(tmp_path, "pkg/__init__.py", "from .models import Thing\n")

    result = _run(tmp_path)

    assert result.returncode == 1
    assert "__init__.py:1" in result.stdout
    assert "_models" in result.stdout


def test_same_directory_class_import_from_private_module_is_accepted(
    tmp_path: pathlib.Path,
) -> None:
    _write(tmp_path, "pkg/_models.py", "class Thing:\n    pass\n")
    _write(tmp_path, "pkg/__init__.py", "from ._models import Thing\n")

    result = _run(tmp_path)

    assert result.returncode == 0, result.stdout


def test_wildcard_relative_import_is_rejected(tmp_path: pathlib.Path) -> None:
    _write(tmp_path, "pkg/example.py", "router = 1\n")
    _write(tmp_path, "pkg/__init__.py", "from .example import *\n")

    result = _run(tmp_path)

    assert result.returncode == 1
    assert "__init__.py:1" in result.stdout


def test_clean_tree_reports_nothing(tmp_path: pathlib.Path) -> None:
    _write(tmp_path, "app.py", "import logging\n\nlog = logging.getLogger(__name__)\n")

    result = _run(tmp_path)

    assert result.returncode == 0
    assert result.stdout.strip() == ""


def test_repository_sources_pass_the_checker() -> None:
    root = pathlib.Path(__file__).resolve().parents[1]

    result = subprocess.run(
        [sys.executable, str(CHECKER)],
        capture_output=True,
        text=True,
        check=False,
        cwd=root,
    )

    assert result.returncode == 0, result.stdout
