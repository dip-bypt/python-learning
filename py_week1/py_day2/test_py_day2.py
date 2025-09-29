import unittest
from unittest.mock import patch, mock_open
import builtins
import sys
from py_day2 import main as py_day2_main

class TestPyDay2(unittest.TestCase):
    def setUp(self):
        self.csv_content = 'name,age\nAlice,17\nBob,19\nCharlie,20\nDavid,16\n'

    @patch('builtins.open', new_callable=mock_open, read_data='name,age\nAlice,17\nBob,19\nCharlie,20\nDavid,16\n')
    @patch('builtins.print')
    def test_students_older_than_18(self, mock_print, mock_file):
        py_day2_main.main()
        mock_print.assert_any_call('Students older than 18:')
        mock_print.assert_any_call('-', 'Bob')
        mock_print.assert_any_call('-', 'Charlie')
        calls = [call.args for call in mock_print.call_args_list]
        names = [c[1] for c in calls if len(c) > 1]
        self.assertNotIn('Alice', names)
        self.assertNotIn('David', names)

if __name__ == '__main__':
    unittest.main()
