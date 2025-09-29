import unittest
import subprocess
import sys
import os

class TestPyDay2(unittest.TestCase):
    def setUp(self):
        # Create a temporary students.csv file in the same directory as main.py
        self.csv_path = os.path.join(os.path.dirname(__file__), 'students.csv')
        with open(self.csv_path, 'w') as f:
            f.write('name,age\nAlice,17\nBob,19\nCharlie,20\nDavid,16\n')

    def tearDown(self):
        # Remove the temporary file after test
        if os.path.exists(self.csv_path):
            os.remove(self.csv_path)

    def test_students_older_than_18(self):
        result = subprocess.run([
            sys.executable, os.path.join(os.path.dirname(__file__), 'main.py')
        ], capture_output=True, text=True)
        output = result.stdout
        self.assertIn('Students older than 18:', output)
        self.assertIn('- Bob', output)
        self.assertIn('- Charlie', output)
        self.assertNotIn('- Alice', output)
        self.assertNotIn('- David', output)

if __name__ == '__main__':
    unittest.main()
