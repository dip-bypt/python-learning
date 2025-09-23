# Python Training - Day 1

## What I practiced
- **Checked Python version** using `sys.version`.
- **Listed installed packages** by running `python -m pip list` through `subprocess.run` with the current interpreter from `sys.executable`.

## Why this matters
- Knowing the active Python version helps avoid environment confusion.
- Seeing installed packages verifies the environment and helps reproduce setups.

## How it works (from `py_day1/py_day1.py`)
- Imports `sys` and `subprocess`.
- Prints the current Python version.
- Executes `pip list` via `[sys.executable, "-m", "pip", "list"]` and prints the captured output.
- Catches and prints any exceptions during the subprocess call.

## How to run
1. Activate the virtual environment (if you created one):
   - macOS/Linux: `source py_week1/ai-env/bin/activate`
   - Windows (PowerShell): `py_week1/ai-env/Activate.ps1`
2. From the project root, run:
   
   ```bash
   python py_week1/py_day1/py_day1.py
   ```

## Expected output (example)
- A line with the current Python version, e.g. `Python version: 3.13.x ...`
- A table of installed packages similar to `pip list` output.

## Notes / tips
- If `pip` output looks empty or errors, ensure the venv is activated and `pip` is available for this interpreter: `python -m pip --version`.
- Use `which python` (macOS/Linux) or `Get-Command python` (PowerShell) to confirm you’re calling the expected interpreter.
