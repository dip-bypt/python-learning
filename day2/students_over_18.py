"""
Day 2: Python Core - Data Structures

This script reads a CSV file containing student names and ages, then prints the names of students older than 18 using a list comprehension.

Key Concepts Demonstrated:
- Reading CSV files using Python's built-in csv module
- Using lists and dictionaries to store data
- List comprehensions for concise data filtering
- Basic file handling
"""

import csv

# Step 1: Read the CSV file and store student data
students = []  # This will be a list of dictionaries, each representing a student
with open('day2/students.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Each row is a dictionary: {'name': ..., 'age': ...}
        # Convert age from string to integer for comparison
        row['age'] = int(row['age'])
        students.append(row)

# Step 2: Use a list comprehension to filter students older than 18
# List comprehensions are a concise way to create lists based on existing lists
older_students = [student['name'] for student in students if student['age'] > 18]

# Step 3: Print the result
print("Students older than 18:")
for name in older_students:
    print(name)

# Explanation:
# - The csv.DictReader reads each row as a dictionary, making it easy to access columns by name.
# - We convert the 'age' field to an integer for numeric comparison.
# - The list comprehension filters and collects names in a single line.
