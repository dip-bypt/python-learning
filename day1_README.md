# Day 1: Python Setup & Environment

## Overview
This project covers the basics of setting up Python 3.11+, creating virtual environments, understanding Python file structure, and installing libraries with pip. It includes creating an `ai-env` virtual environment, installing FastAPI, Uvicorn, and Pandas, and printing the Python version and installed packages.

## Files Included
- `day1.py`: The main Python script that prints the Python version and lists installed packages.
- `day1_readme.md`: This guideline file.

## Prerequisites
- Python 3.11+ installed on your system.
- Basic knowledge of command line.

## Step-by-Step Guide

### 1. Setup
- Ensure you are in the project directory: `/Users/bypti703/Documents/GENERAL_DETAILS/Python_Learning`.
- The file `day1.py` should be present.

### 2. Create a Virtual Environment
- Open a terminal in VSCode or your system.
- Navigate to the project directory.
- Create a virtual environment named `ai-env`:
  ```
  python3 -m venv ai-env
  ```

### 3. Activate the Virtual Environment
- Activate the virtual environment:
  ```
  source ai-env/bin/activate
  ```
- You should see `(ai-env)` in your terminal prompt.

### 4. Install Required Libraries
- Install the required libraries using pip:
  ```
  pip install fastapi uvicorn pandas
  ```

### 5. Running the Script
- Run the script using Python:
  ```
  python day1.py
  ```
- Expected Output:
  ```
  Python Version: 3.11.5
  Installed Packages:
  fastapi==0.104.1
  uvicorn==0.24.0
  pandas==2.1.3
  ```

### 6. Code Explanation
- **Import Statements**: `import sys` and `import pkg_resources` - Used to get Python version and list installed packages.
- **Print Python Version**: `sys.version` - Prints the current Python version.
- **List Installed Packages**: `pkg_resources.working_set` - Gets the list of installed packages and their versions.

### 7. Troubleshooting
- **Virtual Environment Not Activating**: Ensure you are using the correct activation command for your OS (e.g., `ai-env\Scripts\activate` on Windows).
- **Library Installation Errors**: Check your internet connection and Python version compatibility.
- **Script Not Running**: Ensure you are in the correct directory and have activated the virtual environment.

## Learning Outcomes
- Learned how to create and activate virtual environments.
- Understood how to install libraries using pip.
- Practiced Python file structure and script execution.

## Next Steps
- Explore more about virtual environments and package management.
- Move on to Day 2 for data structures and list comprehensions.
