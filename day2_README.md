# Day 2: Python Core - Data Structures and List Comprehensions

## Overview
This project demonstrates reading a CSV file containing student data (name and age) and using a list comprehension to filter and print names of students older than 18. It aligns with Day 2 learning objectives: Strings, Lists, Tuples, Sets, Dicts, List comprehensions & lambda functions, Looping & iteration patterns.

## Files Included
- `day2.py`: The main Python script that reads the CSV file and processes the data.
- `students.csv`: A sample CSV file with student data (name and age).
- `README.md`: This guideline file.

## Prerequisites
- Python 3.x installed on your system.
- FastAPI and uvicorn installed (pip install fastapi uvicorn).

## Step-by-Step Guide

### 1. Setup
- Ensure you are in the project directory: `/Users/bypti703/Documents/GENERAL_DETAILS/Python_Learning`.
- The files `day2.py` and `students.csv` should be present.

### 2. Understanding the CSV File
- Open `students.csv` to view the data structure:
  - First row: Headers (`name`, `age`)
  - Subsequent rows: Student records (e.g., Alice,20)
- Sample data:
  ```
  name,age
  Alice,20
  Bob,17
  Charlie,22
  Diana,19
  Eve,16
  ```

### 3. Running the Server
- Open a terminal in VSCode or your system.
- Navigate to the project directory.
- Run the server using uvicorn:
  ```
  uvicorn day2:app --reload
  ```
- The server will start on http://127.0.0.1:8000.
- Test the endpoint by visiting http://127.0.0.1:8000/students/older-than-18 in your browser or using curl:
  ```
  curl http://127.0.0.1:8000/students/older-than-18
  ```
- Expected Output:
  ```
  {"older_students": ["Alice", "Charlie", "Diana"]}
  ```

### 4. Code Explanation
- **Import Statement**: `from fastapi import FastAPI` and `import csv` - Imports FastAPI for the web framework and CSV for reading the file.
- **App Instance**: `app = FastAPI()` - Creates the FastAPI application.
- **Endpoint**: `@app.get("/students/older-than-18")` - Defines a GET endpoint.
- **Function**: `def get_older_students()` - The function that reads the CSV, filters the data using list comprehension, and returns the result as JSON.
- **List Comprehension**: `[student['name'] for student in csv_reader if int(student['age']) > 18]` - Filters the names of students older than 18.

### 5. Customization
- **Modify CSV Data**: Edit `students.csv` to add, remove, or change student records. Ensure the format remains `name,age`.
- **Change File Name**: If you want to use a different CSV file, update the file name in `day2.py` (e.g., change `'students.csv'` to `'your_file.csv'`).
- **Adjust Age Threshold**: Modify the condition in the list comprehension (e.g., change `> 18` to `>= 20`).

### 6. Troubleshooting
- **Server Not Starting**: Ensure FastAPI and uvicorn are installed.
- **File Not Found Error**: Ensure `students.csv` is in the same directory as `day2.py`.
- **ValueError on Age**: Ensure all age values in the CSV are numeric (e.g., 20, not 'twenty').
- **No Output**: Check if there are students older than 18 in your CSV data.

## Learning Outcomes
- Practiced reading CSV files using Python's `csv` module.
- Applied list comprehensions for filtering data.
- Understood iteration patterns and conditional logic in Python.

## Next Steps
- Experiment with lambda functions or other data structures (e.g., dictionaries) based on Day 2 topics.
- Extend the script to handle more columns or perform additional operations (e.g., calculate average age).
