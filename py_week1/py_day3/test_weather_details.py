import unittest
from unittest.mock import patch, mock_open, MagicMock
import builtins
import sys
import os
import json
from py_week1.py_day3 import weather_details

class TestWeatherDetails(unittest.TestCase):
    @patch('requests.get')
    @patch('builtins.open', new_callable=mock_open)
    @patch('builtins.print')
    def test_successful_response(self, mock_print, mock_file, mock_get):
        # Mock API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'current': {
                'temp_c': 30,
                'humidity': 50,
                'pressure_mb': 1000,
                'wind_kph': 10,
                'last_updated': '2025-09-29 12:00',
                'condition': {'text': 'Sunny'}
            }
        }
        mock_get.return_value = mock_response
        # Mock file read/write
        handle = mock_file()
        handle.read.return_value = json.dumps(mock_response.json.return_value)
        # Run script
        weather_details.main()
        # Check print calls for temperature and humidity
        calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(any('Temperature: 30 C' in c for c in calls))
        self.assertTrue(any('Humidity: 50 %' in c for c in calls))
        self.assertTrue(any('Weather Report: Sunny' in c for c in calls))

    @patch('requests.get')
    @patch('builtins.open', new_callable=mock_open)
    @patch('builtins.print')
    def test_keyerror_handling(self, mock_print, mock_file, mock_get):
        # Mock API response missing 'current'
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response
        handle = mock_file()
        handle.read.return_value = json.dumps({})
        weather_details.main()
        calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(any('Error: Key not found' in c for c in calls))

    @patch('requests.get')
    @patch('builtins.print')
    def test_http_error_handling(self, mock_print, mock_get):
        # Mock API response with error status
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        weather_details.main()
        calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(any('Error in the HTTP request' in c for c in calls))

if __name__ == '__main__':
    unittest.main()
