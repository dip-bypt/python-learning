#!/usr/bin/env python3
import sys
import subprocess

class Day1:
    def __call__(self):
        """
        Day 1 Task: Print Python version and installed packages.
        """
        python_executable = sys.executable
        python_version = sys.version.splitlines()[0]
        # Run pip list and capture the output
        pip_list = subprocess.run(
            [sys.executable, "-m", "pip", "list"], capture_output=True, text=True
        ).stdout

        # Print the results
        print("Python Executable:", python_executable)
        print("Python Version:", python_version)
        print("\nInstalled Packages:")
        print(pip_list)

# Create an instance of the Day1 class
app = Day1()