# Python Training - Day 2

## What I practiced
- **Reading CSV data with pandas** into a `DataFrame` from `students.csv`.
- **Exploring tabular data** by printing the DataFrame.
- **List comprehension with filtering** to build a list of student names with `age > 18`.

## Dataset
- File: `py_week1/py_day2/students.csv`
- Example columns observed: `studentId`, `name`, `age`, `grade`, `email`.

## How it works (from `py_week1/py_day2/main.ipynb`)
- `import pandas as pd`
- `df = pd.read_csv('students.csv')` reads the CSV in the notebook's directory.
- `print(df)` displays the full table.
- `names_over_18 = [name for name, age in zip(df['name'], df['age']) if age > 18]` creates the filtered list.
- `print(names_over_18)` shows the resulting names.

## How to run
1. Activate your environment (optional but recommended):
   - macOS/Linux: `source py_week1/ai-env/bin/activate`
   - Windows (PowerShell): `py_week1/ai-env/Activate.ps1`
2. Open Jupyter Lab/Notebook from the project root:
   
   ```bash
   jupyter lab
   ```
   
   or
   
   ```bash
   jupyter notebook
   ```
3. In the UI, open `py_week1/py_day2/main.ipynb`, run the cells in order.

## Expected output (example)
- Printed DataFrame, e.g. a table of 10 students with columns above.
- A Python list of names older than 18, e.g.:

  ```python
  ['Alice Johnson', 'Bob Smith', 'Charlie Brown', 'Ethan Hunt', 'Fiona Gallagher', 'Hannah Lee']
  ```

## Notes / tips
- Ensure `pandas` is installed in your environment: `python -m pip install pandas`.
- If the CSV path fails, verify the working directory. From within the notebook, run:
  
  ```python
  import os; print(os.getcwd())
  ```
  
  The file should be located at `py_week1/py_day2/students.csv` relative to the project root.
- You can extend the analysis: compute averages, group by `grade`, validate email formats, etc.
