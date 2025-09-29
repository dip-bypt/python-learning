import unittest
import subprocess
import sys
import os

class TestPyDay1(unittest.TestCase):
    def test_prints_python_version_and_packages(self):
        # Run the script as a subprocess
        result = subprocess.run([
            sys.executable, os.path.join(os.path.dirname(__file__), 'py_day1.py')
        ], capture_output=True, text=True)
        output = result.stdout
        self.assertIn('Python version:', output)
        self.assertIn('Installed packages:', output)
        # Should list at least one package (pip itself)
        self.assertIn('pip', output)

    def test_error_handling(self):
        # Temporarily rename pip to simulate error
        import shutil
        pip_path = shutil.which('pip')
        if pip_path:
            temp_path = pip_path + '_bak'
            os.rename(pip_path, temp_path)
            try:
                result = subprocess.run([
                    sys.executable, os.path.join(os.path.dirname(__file__), 'py_day1.py')
                ], capture_output=True, text=True)
                output = result.stdout + result.stderr
                self.assertIn('Error getting package list:', output)
            finally:
                os.rename(temp_path, pip_path)
        else:
            self.skipTest('pip not found in environment')

if __name__ == '__main__':
    unittest.main()
