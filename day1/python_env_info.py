"""
Day 1: Python Setup & Environment
This script prints the current Python version and lists all installed packages in the environment.

Steps performed:
1. Print the Python version using sys and platform modules.
2. List all installed packages using pip's internal API.
"""

import sys
import platform

# Print Python version
def print_python_version():
    print("Python Version:")
    print(platform.python_version())
    print(f"(Detailed: {sys.version})\n")

# List installed packages
def list_installed_packages():
    print("Installed Packages:")
    try:
        import pkg_resources
        packages = sorted([f"{d.project_name}=={d.version}" for d in pkg_resources.working_set])
        for pkg in packages:
            print(pkg)
    except ImportError:
        print("pkg_resources not found. Try running 'pip list' in the terminal.")

if __name__ == "__main__":
    print_python_version()
    list_installed_packages()
