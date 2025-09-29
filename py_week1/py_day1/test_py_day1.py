import unittest
from unittest.mock import patch, MagicMock
import sys
import builtins
from py_day1 import py_day1

class TestPyDay1(unittest.TestCase):
    @patch('subprocess.run')
    def test_prints_python_version_and_packages(self, mock_run):
        mock_result = MagicMock()
        mock_result.stdout = 'package1 1.0.0\npackage2 2.0.0\n'
        mock_run.return_value = mock_result
        with patch('builtins.print') as mock_print:
            py_day1.main()
            mock_print.assert_any_call('Python version:', sys.version)
            mock_print.assert_any_call('\nInstalled packages:')
            mock_print.assert_any_call('package1 1.0.0\npackage2 2.0.0\n')

    @patch('subprocess.run', side_effect=Exception('fail'))
    def test_error_handling(self, mock_run):
        with patch('builtins.print') as mock_print:
            py_day1.main()
            self.assertTrue(any('Error getting package list:' in str(call) for call in mock_print.call_args_list))

if __name__ == '__main__':
    unittest.main()
