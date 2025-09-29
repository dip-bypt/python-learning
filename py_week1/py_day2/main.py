# py_day2/py_day2.py
"""
Day 2 Training Task:
--------------------
1. Read a CSV file of students (name, age).
2. Print names of students older than 18 using a list comprehension.

Core Python Concepts Covered:
-----------------------------
- Strings: student names are strings (text).
- Lists: we will store student records in a list.
- Dicts: each row from CSV is read as a dictionary (column name -> value).
- List Comprehensions: a short way to create lists in one line.
- Looping & Iteration: list comprehension is a loop written in compact form.

How to Run:
-----------
1. Create a CSV file named "students.csv" inside the py_day2/ folder.
   Example content of students.csv:
       name,age
       Alice,17
       Bob,19
       Charlie,20
       David,16

2. Run the Python script:
       python py_week1/py_day2/main.py
"""

import csv  # CSV module helps us read/write CSV files easily

# Step 1: Open and read the CSV file
with open("students.csv", mode="r") as file:
    reader = csv.DictReader(file)
    # DictReader reads each row as a dictionary, e.g. {"name": "Alice", "age": "17"}

    # Step 2: Convert reader object into a list of dictionaries
    students = list(reader)

# Step 3: Use list comprehension to get names of students older than 18
# Note: int(row["age"]) converts the "age" string into an integer
older_students = [row["name"] for row in students if int(row["age"]) > 18]

# Step 4: Print the result
print("Students older than 18:")
for name in older_students:
    print("-", name)
