You just move your dependencies into `pyproject.toml` under `dependencies`. Then a single `pip install -e .` installs both your project **and** all libraries at once — no more manual `pip install -r` step.

Here's your complete `pyproject.toml` with all your libraries from `dependencies.txt`:

```toml
[build-system]
requires = ["setuptools"]
build-backend = "setuptools.backends.legacy:build"

[project]
name = "plecs-automation"
version = "0.1.0"
description = "PLECS simulation automation toolkit"
requires-python = ">=3.9"

dependencies = [
    # ── Numerical & Scientific ─────────────────────────────
    "numpy==1.22.4",
    "scipy==1.10.1",
    "pandas==2.2.2",
    "sympy==1.12",
    "scikit-learn==1.2.2",

    # ── Visualization ──────────────────────────────────────
    "matplotlib==3.6.2",
    "plotly==5.11.0",

    # ── Networking & Serialization ─────────────────────────
    "json-rpc==1.13.0",
    "jsonrpc-requests==0.4.0",

    # ── Data & Utilities ───────────────────────────────────
    "natsort==8.2.0",
    "more_itertools==9.1.0",
    "flatdict==4.0.1",
    "unflatten==0.1.1",

    # ── CLI & Formatting ───────────────────────────────────
    "pyfiglet==0.8.post1",
    "termcolor==1.1.0",

    # ── System & Process ───────────────────────────────────
    "psutil==5.9.2",

    # ── Platform-Specific : Windows ────────────────────────
    "pywin32==304",
    "pywinauto==0.6.8",
]

[tool.setuptools.packages.find]
where = ["."]
include = ["Script*"]
```

Then just run **once** at project root:

```bash
pip install -e .
```

The `-e` means **editable mode** — your `Script/` code is linked in-place, so changes to your files take effect immediately without reinstalling.

---

A few notes specific to your setup:

**Pin vs. unpinned** — you're currently pinning exact versions (`==`). That's good for reproducibility in an engineering/simulation context like PLECS automation where you want deterministic behavior. Keep it.

**`pywin32` / `pywinauto`** — these are Windows-only. If you ever need to guard against that:
```toml
"pywin32==304 ; sys_platform == 'win32'",
"pywinauto==0.6.8 ; sys_platform == 'win32'",
```

**Your old `dependencies.txt`** — you can keep it as a reference or delete it. If you want to generate it automatically from your `pyproject.toml` in the future:
```bash
pip freeze > dependencies.txt
```


You need a **wheelhouse** — a folder of pre-downloaded `.whl` files that pip installs from locally, no internet needed.

## Step 1 — Download all wheels onto your machine (online, once)

```bash
pip download -r dependencies.txt -d wheelhouse/
```

This creates a `wheelhouse/` folder at your project root with every `.whl` file in it.

---

## Step 2 — Project structure

```
project_root/
├── pyproject.toml
├── main.py
├── wheelhouse/          ← all .whl files live here
│   ├── numpy-1.22.4-cp39-win_amd64.whl
│   ├── pandas-2.2.2-cp39-win_amd64.whl
│   └── ...
├── Script/
│   ├── __init__.py
│   └── ...
```

---

## Step 3 — Update `pyproject.toml` to point to the wheelhouse

```toml
[build-system]
requires = ["setuptools"]
build-backend = "setuptools.backends.legacy:build"

[project]
name = "plecs-automation"
version = "0.1.0"
description = "PLECS simulation automation toolkit"
requires-python = ">=3.9"

dependencies = [
    # ── Numerical & Scientific ─────────────────────────────
    "numpy==1.22.4",
    "scipy==1.10.1",
    "pandas==2.2.2",
    "sympy==1.12",
    "scikit-learn==1.2.2",

    # ── Visualization ──────────────────────────────────────
    "matplotlib==3.6.2",
    "plotly==5.11.0",

    # ── Networking & Serialization ─────────────────────────
    "json-rpc==1.13.0",
    "jsonrpc-requests==0.4.0",

    # ── Data & Utilities ───────────────────────────────────
    "natsort==8.2.0",
    "more_itertools==9.1.0",
    "flatdict==4.0.1",
    "unflatten==0.1.1",

    # ── CLI & Formatting ───────────────────────────────────
    "pyfiglet==0.8.post1",
    "termcolor==1.1.0",

    # ── System & Process ───────────────────────────────────
    "psutil==5.9.2",

    # ── Platform-Specific : Windows ────────────────────────
    "pywin32==304 ; sys_platform == 'win32'",
    "pywinauto==0.6.8 ; sys_platform == 'win32'",
]

[tool.setuptools.packages.find]
where = ["."]
include = ["Script*"]

# ── Tell pip where to find packages locally ────────────────
[tool.pip]
find-links = ["wheelhouse"]
no-index = true
```

---

## Step 4 — Add an `install.bat` for the user (one double-click setup)

```bat
@echo off
echo Installing PLECS Automation project...
pip install --no-index --find-links=wheelhouse -e .
echo Done! You can now run main.py
pause
```

The user just clones/copies the folder and double-clicks `install.bat`. No internet, no pip config, nothing else needed.

---

## Important note on wheels

Wheels are **platform and Python version specific**. The filename tells you what it targets:

```
numpy-1.22.4-cp39-cp39-win_amd64.whl
              ^^^^         ^^^^^^^^
           Python 3.9     Windows 64-bit
```

So download the wheels **on the same OS and Python version** your users will have. If they all run Windows + Python 3.9 (which is likely in a BMW engineering context), you're fine. If versions differ, you'd need to download wheels per target.



Roughly **150–300 MB** depending on transitive dependencies. Here's the breakdown:

## Your heavy hitters
| Package | Approx size |
|---|---|
| `scipy` | ~35 MB |
| `numpy` | ~15 MB |
| `pywin32` | ~12 MB |
| `pandas` | ~15 MB |
| `scikit-learn` | ~8 MB |
| `matplotlib` | ~7 MB |
| `plotly` | ~5 MB |
| `sympy` | ~6 MB |
| Everything else | ~5 MB |
| **Direct deps total** | **~108 MB** |

## The hidden cost — transitive dependencies
`pip download` also pulls **dependencies of your dependencies** automatically. For example:
- `matplotlib` pulls → `pillow`, `kiwisolver`, `pyparsing`, `cycler`
- `pandas` pulls → `python-dateutil`, `pytz`
- `scikit-learn` pulls → `joblib`, `threadpoolctl`
- `pywinauto` pulls → `comtypes`, `six`

That adds roughly another **50–150 MB** on top.

---

## Check the exact size before committing

Run this after downloading:

```bash
pip download -r dependencies.txt -d wheelhouse/

# Windows
du -sh wheelhouse/        # Git Bash
# or
powershell -command "(Get-ChildItem wheelhouse | Measure-Object -Property Length -Sum).Sum / 1MB"
```

---

## If size is a problem

**Option 1 — `.gitignore` the wheelhouse, document the download step**
```gitignore
# .gitignore
wheelhouse/
```
Then in your `README.md`:
```
Run once (requires internet):
    pip download -r dependencies.txt -d wheelhouse/

Then for all future installs (offline):
    install.bat
```

**Option 2 — Share via network drive / USB** instead of git, which is probably more realistic in a BMW engineering environment where you're distributing to colleagues on the same internal network anyway.

**Option 3 — Use a local PyPI mirror** like `devpi` if your team has a server — this is the enterprise-grade solution and common in automotive/industrial environments with strict network policies.




Great question. They solve **different problems** — the wheelhouse handles *distribution*, venv handles *isolation*. You actually want both together.

## What wheelhouse gives you
- 📦 Offline installation
- 🚀 One-click setup for users
- 📌 Pinned versions shipped with the project

## What venv adds on top

| Problem | Without venv | With venv |
|---|---|---|
| **Isolation** | Libraries install into system Python, shared with every other project | Each project gets its own private Python environment |
| **Version conflicts** | Project A needs `numpy==1.22`, Project B needs `numpy==1.26` → one breaks | Both coexist peacefully |
| **Clean uninstall** | To remove, you'd have to unpick every installed lib manually | Delete the `venv/` folder, done |
| **Reproducibility** | "Works on my machine" | Everyone runs the exact same isolated environment |
| **No admin rights needed** | May need system-level permissions | Always installs into user space |

---

## The right setup uses both together

Update your `install.bat` to create a venv first:

```bat
@echo off
echo Creating virtual environment...
python -m venv venv

echo Activating...
call venv\Scripts\activate.bat

echo Installing packages from wheelhouse...
pip install --no-index --find-links=wheelhouse -e .

echo.
echo Done! To run the project:
echo   1. call venv\Scripts\activate.bat
echo   2. python main.py
pause
```

And add `venv/` to `.gitignore` — you never commit the venv itself:
```gitignore
venv/
__pycache__/
*.pyc
```

---

## Mental model

Think of it like this:
- **wheelhouse** = the box of ingredients you ship to the user
- **venv** = the kitchen where those ingredients get used, kept separate from everyone else's kitchen

Without venv, you're cooking in a shared kitchen where someone else's spices might clash with yours.