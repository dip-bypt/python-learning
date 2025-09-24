#!/usr/bin/env python3
import csv

class Day2:
    def __call__(self):
        """
        Day 2 Task: Read CSV file and print names of students older than 18 using list comprehension.
        """
        with open('day2_students.csv', mode='r') as file:
            csv_reader = csv.DictReader(file)
            older_students = [student['name'] for student in csv_reader if int(student['age']) > 18]
            print("Names of students older than 18:")
            for name in older_students:
                print(name)

# Create an instance of the Day2 class
app = Day2()
