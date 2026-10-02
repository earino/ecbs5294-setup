# ECBS5294 — Setup check

**Working with Data · due before Session 1 (Monday 5 October 2026)**

## Start here

| | |
|---|---|
| **What this is** | The path every lab and homework in this course takes, done once, on a project that is not broken: clone, sync, run a check, run a notebook, commit, archive, submit. |
| **What it checks** | Python from this project's `.venv`; DuckDB **1.5.5**; one query on a real data file; Git and your Git identity; on Windows, Git Bash. |
| **What you hand in** | `setup-submission.zip` and the check's output, to the Moodle **Setup verification** slot. |
| **How long** | About fifteen minutes on a laptop that did DS1. |
| **Did not take DS1?** | Do the course site's **Bridge from DS1** page first. Its exercises are practice; this check is the evidence. Then book a supported rehearsal (step 6). |

Session 1 cannot be tech support. If a step fails and the fix printed beside it does not work, submit what you have
anyway, with the output, and say so in the Moodle text box: it tells us exactly what to help with. Then book a
supported rehearsal with a TA (step 6).

## 1. Get the project (terminal)

Open your terminal: **Git Bash** on Windows (not PowerShell, not cmd), Terminal on macOS. Go to the folder where you
keep course work, then:

```bash
git clone https://github.com/earino/ecbs5294-setup.git
cd ecbs5294-setup
uv sync
```

`uv sync` builds this project's environment in `.venv/`, with DuckDB in it. Nothing is installed anywhere else, and
every lab in this course does the same.

## 2. Run the check (terminal)

From the same folder:

```bash
uv run python check.py
```

It prints one line per check and ends in **`ALL CHECKS PASSED`**, or in **`FIX THESE FIRST`** with one line per
problem and what to do about it. Fix, run it again. When it passes, save its output in a file:

```bash
uv run python check.py > check_output.txt
cat check_output.txt
```

`>` sends the output into the file instead of the screen; `cat` shows you the file.

## 3. Run the notebook (VS Code)

A script that runs in the terminal does not prove that VS Code can run a cell. So run one.

1. Open **this folder** in VS Code (*File → Open Folder…*, not the notebook file). If VS Code asks whether you trust
   the authors, choose **Yes, I trust the authors**.
2. Open `check_notebook.ipynb`.
3. Click **Select Kernel** (top right) → *Python Environments…* → the entry marked **Recommended** whose path contains
   **`.venv`**.
4. **Run All.** Three outputs appear: a path containing `.venv`, `duckdb 1.5.5`, and a table with **525461** in it.
5. **Save** the notebook (Ctrl+S, or Cmd+S on a Mac). Outputs you see on screen are in the file only after a save.
6. **Prove it.** Back in the terminal, run `uv run python check.py` again: the line `notebook has saved outputs` must
   now say **yes**. If it says *no*, the file has no outputs: go back to step 4, Run All, and save. Then save the
   output again, `uv run python check.py > check_output.txt`, so the file you hand in shows the yes.

## 4. Commit (terminal)

```bash
git status
```

It lists `check_notebook.ipynb` as *modified* (it has outputs now) and `check_output.txt` as *untracked* (Git has
never seen it). **If `check_notebook.ipynb` is not listed as modified, the outputs were not saved: back to step 3.**
Commit both:

```bash
git add check_output.txt check_notebook.ipynb
git commit -m "Setup check passes on my laptop: duckdb 1.5.5, 525,461 rows"
git status
```

The last `git status` must say *nothing to commit, working tree clean*. If `git commit` says it does not know who you
are, the check's `git user.name` or `git user.email` line told you the command to run.

## 5. Make the archive (terminal)

```bash
git archive --format=zip -o ../setup-submission.zip HEAD
```

`git archive` packs the files of your last commit, and nothing Git ignores (`.venv/` is ignored), into one zip. It
writes it in the folder **above** the project, so the zip never ends up inside it. Every homework in this course is
submitted this way. Look inside:

```bash
uv run python -c "import zipfile; print(*zipfile.ZipFile('../setup-submission.zip').namelist(), sep='\n')"
```

The list must include `check_output.txt` and `check_notebook.ipynb`. It must not include `.venv/`. The zip is about
3 MB: most of it is the data file, which is committed on purpose.

## 6. Submit (Moodle)

In the Moodle **Setup verification** slot:

- upload `setup-submission.zip` (it is in the folder above `ecbs5294-setup`);
- in the text box, write three things: the contents of `check_output.txt`, pasted; **whether you took DS1**; and
  **roughly how long setup took you**, from the first install to this upload.

**If you did not take DS1, or a check failed, or setup took you more than an hour:** book a supported 30-minute
rehearsal with a TA in the week before Session 1, on Moodle. You run this path once more with someone beside you, so
that Session 1's lab is about the data, not the tools. It is there to help, not to test you.

That is the whole path. Lab 1 starts the same way: clone, `uv sync`, open the folder, pick the `.venv` kernel.

## What each check means

| Line | What it proves | If it fails |
|---|---|---|
| `python (this one)`, `inside this project's .venv` | `uv run` used this project's own Python | Run it as `uv run python check.py`, from this folder |
| `not the Store stub` (Windows) | `python` is a real interpreter | Turn off the two App execution aliases for Python in Windows Settings |
| `import duckdb` = 1.5.5 | the course's exact DuckDB is in this environment | `uv sync`, then run the check again with `uv run` |
| `import pandas`, `import ipykernel` | notebooks can run here and show a table | `uv sync` |
| `query the data file` | DuckDB read a real file from a path relative to this folder | Run from this folder, the one with `pyproject.toml` in it |
| `git`, `uv` | the tools are on your PATH | Install them: the course site's *Pre-course setup* page links the steps |
| `git user.name`, `git user.email` | Git can record who made a commit | Run the `git config --global …` line the check prints |
| `shell is Git Bash`, `core.autocrlf = input` (Windows) | the course's one shell and line-ending setting | Open Git Bash; run the `git config` line the check prints |

The two `[--]` lines are information, not checks. `notebook has saved outputs` says *no* until you have done step 3
and saved; after that it must say *yes*, and that is the proof the notebook step worked. `this folder is a Git clone`
says *no* if you downloaded a ZIP from GitHub instead of cloning, and then step 4 will fail: clone it (step 1).

## Windows notes

- **Never type bare `python` in Git Bash.** On some setups it hangs with no error. Always give it something to run:
  `python --version`, `uv run python check.py`.
- If the check reports a path containing `WindowsApps`, that is the Microsoft Store stub, not Python: *Settings → Apps
  → Advanced app settings → App execution aliases*, turn off both `python` entries, run the check again.
- VS Code's terminal should be Git Bash too: Command Palette → *Terminal: Select Default Profile* → **Git Bash**.

## If you got lost: start again

The setup check has nothing in it worth keeping. Delete the `ecbs5294-setup` folder (and `setup-submission.zip`, if
you made one) and start again from step 1.
