# py_day1/py_day1.py
"""
Day 1 Training Task:
--------------------
1. Print Python version.
2. List installed packages (using pip).

How this works:
---------------
- We import 'sys' to access the current Python runtime (to know the version).
- We import 'subprocess' to run shell commands inside Python.
- 'subprocess.run()' executes 'python -m pip list'
  using the current Python interpreter (sys.executable).
- We capture the output and print it nicely.

How to run:
-----------
# Make sure you are inside your project folder and the virtual environment (ai-env) is activated.

Command:
    python py_week1/py_day1/py_day1.py
"""

import sys
import subprocess

# Print the current Python version
print("Python version:", sys.version)

print("\nInstalled packages:")

try:
    # Run "python -m pip list" and capture the output
    result = subprocess.run(
        [sys.executable, "-m", "pip", "list"],
        capture_output=True,   # Capture the command output
        text=True              # Decode output as string (instead of bytes)
    )

    # Print the list of installed packages
    print(result.stdout)

except Exception as e:
    # In case something goes wrong, print the error
    print(f"Error getting package list: {e}")
