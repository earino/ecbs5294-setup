"""ECBS5294 setup check.

Run it from this project folder, the one with pyproject.toml in it:

    uv run python check.py

It prints one line per check. The last lines say ALL CHECKS PASSED, or FIX THESE FIRST with one line per problem.
It uses the standard library and DuckDB only.
"""

from __future__ import annotations

import os
import platform
import re
import shutil
import subprocess
import sys
from pathlib import Path

# A path with any letter in it (a user folder called Szoke with an accent, say) must print on any Windows code page.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(errors="backslashreplace")

DUCKDB_PIN = "1.5.5"                         # the version every lab and homework pins, exactly
DATA = "data/raw/online_retail.parquet"      # a relative path: it is read from the folder you run this in
ROWS = 525_461                               # invoice lines in the course's copy of the file

problems: list[str] = []


def line(label: str, value: str, ok: bool, fix: str = "") -> None:
    print(f"  [{'ok' if ok else '!!'}] {label:<30} {value}")
    if not ok:
        problems.append(f"{label}: {fix or value}")


def note(label: str, value: str) -> None:
    """Information only: never a failure."""
    print(f"  [--] {label:<30} {value}")


def first_line(cmd: list[str]) -> tuple[int, str]:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
    except Exception as e:  # noqa: BLE001
        return 1, f"error: {e}"
    out = (r.stdout or r.stderr).strip()
    return r.returncode, (out.splitlines()[0] if out else "")


def semver(text: str) -> tuple[int, ...]:
    m = re.search(r"(\d+)\.(\d+)(?:\.(\d+))?", text)
    return tuple(int(x) for x in m.groups(default="0")) if m else (0,)


print(f"ECBS5294 setup check | {platform.system()} {platform.release()} | {platform.machine()}")
print(f"Running in: {Path.cwd()}\n")

# 1. The Python that `uv run` picked
exe = sys.executable
exe_slash = exe.replace("\\", "/")
py_note = "" if sys.version_info >= (3, 13) else " (works, but below the 3.13 program standard)"
line("python (this one)", f"{platform.python_version()}{py_note}  {exe}", sys.version_info >= (3, 10),
     "this repo pins 3.13 and `uv sync` fetches it: run `uv sync`, then `uv run python check.py`")
line("not the Store stub", "ok" if "WindowsApps" not in exe else exe, "WindowsApps" not in exe,
     "turn off the Microsoft Store python aliases (Settings -> Apps -> Advanced app settings -> "
     "App execution aliases), then re-run")
line("inside this project's .venv", "yes" if ".venv" in exe_slash else exe, ".venv" in exe_slash,
     "run it as `uv run python check.py`, from inside the cloned folder")

# 2. DuckDB, the course's language, at the pinned version, from THIS interpreter
duckdb = None
try:
    import duckdb  # type: ignore[no-redef]

    v = duckdb.__version__
    line("import duckdb", v, v == DUCKDB_PIN,
         f"this Python has duckdb {v}, the course pins {DUCKDB_PIN}: you are not running this project's "
         "environment. Run `uv sync`, then `uv run python check.py` from this folder")
except Exception as e:  # noqa: BLE001
    line("import duckdb", str(e), False, "run `uv sync` in this folder, then `uv run python check.py`")

# 3. pandas shows query results in every lab notebook; ipykernel lets VS Code run a cell on this environment
for mod in ("pandas", "ipykernel"):
    try:
        m = __import__(mod)
        line(f"import {mod}", m.__version__, True)
    except Exception as e:  # noqa: BLE001
        line(f"import {mod}", str(e), False, "run `uv sync` in this folder, then `uv run python check.py`")

# 4. One query on the course's data, with the path every lab uses: relative to the project folder
if duckdb is None:
    line("query the data file", "skipped: duckdb did not import", False, "fix the duckdb line first")
elif not Path(DATA).exists():
    line("query the data file", f"{DATA} not found from {Path.cwd()}", False,
         "run this from the project folder, the one with pyproject.toml in it (cd there first), "
         "not from a folder inside it or above it")
else:
    n = duckdb.connect().sql(f"SELECT COUNT(*) FROM '{DATA}'").fetchone()[0]
    line("query the data file", f"{n:,} rows in {DATA}", n == ROWS,
         f"expected {ROWS:,} rows: this is not the course's copy of the file. Delete the folder and clone again")

# 5. Tools on PATH
for tool, minimum, fix in (
    ("git", (2, 23), "install Git 2.23 or later (Git for Windows on Windows)"),
    ("uv", (0, 4), "install uv: https://docs.astral.sh/uv/"),
):
    found = shutil.which(tool)
    ver = first_line([tool, "--version"])[1] if found else "not on PATH"
    line(tool, ver, bool(found) and semver(ver) >= minimum, fix)

# 6. Git identity: without it, the commit in README step 4 fails
for key in ("user.name", "user.email"):
    code, val = first_line(["git", "config", "--get", key])
    ok = code == 0 and bool(val) and not val.startswith("error")
    placeholder = "YOUR NAME" if key == "user.name" else "YOUR EMAIL"
    line(f"git {key}", val if ok else "(not set)", ok, f'run: git config --global {key} "{placeholder}"')

# 7. The shell
shell = os.environ.get("SHELL", "") or os.environ.get("ComSpec", "")
if platform.system() == "Windows":
    in_git_bash = "MSYSTEM" in os.environ or "bash" in shell.lower()
    line("shell is Git Bash", os.environ.get("MSYSTEM", shell or "unknown"), in_git_bash,
         "open Git Bash (not PowerShell, not cmd) and re-run. In VS Code: Command Palette -> "
         "'Terminal: Select Default Profile' -> Git Bash, then open a new terminal")
    crlf = first_line(["git", "config", "--global", "core.autocrlf"])[1]
    line("core.autocrlf = input", crlf or "(not set)", crlf.strip() == "input",
         "run: git config --global core.autocrlf input")
else:
    line("shell", shell or "unknown", True)

# 8. A Git clone, not a ZIP download (information only: the commit in step 4 needs it)
project = Path(__file__).resolve().parent
code, top = first_line(["git", "-C", str(project), "rev-parse", "--show-toplevel"])
if code == 0 and top and Path(top).resolve() == project:
    note("this folder is a Git clone", "yes")
else:
    note("this folder is a Git clone", "no -- README step 4 needs `git clone`, not a ZIP download")

print()
if problems:
    print("FIX THESE FIRST")
    for p in problems:
        print(f"  - {p}")
    sys.exit(1)
print("ALL CHECKS PASSED")
print("\nNext: the notebook (README step 3), then the commit, the archive, and Moodle (steps 4 to 6).")
