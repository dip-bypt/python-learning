import unittest
from fastapi.testclient import TestClient
from py_week1.py_day4.main import API, encrypt

class TestPyDay4(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(API)

    def test_hello_endpoint(self):
        response = self.client.get('/hello')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Hello, BYPT Fast Api!'})

    def test_login_endpoint(self):
        data = {'email': 'test@example.com', 'password': 'abc'}
        response = self.client.post('/login', json=data)
        self.assertEqual(response.status_code, 200)
        # Password 'abc' encrypted with key=3: 'def'
        self.assertEqual(response.json(), {
            'email': 'test@example.com',
            'encryptedPassword': 'def'
        })

    def test_encrypt_function(self):
        self.assertEqual(encrypt('abc', 3), 'def')
        self.assertEqual(encrypt('ABC', 1), 'BCD')
        self.assertEqual(encrypt('', 5), '')  # Edge case: empty string
        self.assertEqual(encrypt('123', 1), '234')

if __name__ == '__main__':
    unittest.main()

