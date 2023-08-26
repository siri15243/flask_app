from flask_testing import TestCase
import sys
import os
import jwt
import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app


class TestAPI(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app


    def test_valid_input(self):
        token = jwt.encode({'username': 'user1', 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        headers = {'Authorization': 'Bearer ' + token}
        response = self.client.post('/generate_array', json={'sentence': 'Test'}, headers=headers)
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 500)


    def test_response(self):
        token = jwt.encode({'username': 'user1', 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        headers = {'Authorization': 'Bearer ' + token}
        response = self.client.post('/generate_array', json={'sentence': 'Test'}, headers=headers)
        data = response.json
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 500)


    def test_register(self):
        response = self.client.post('/register', json={'username': 'user1', 'password': 'password1'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'User registered already, Please login'})


    def test_login_valid(self):
        response = self.client.post('/login', json={'username': 'user1', 'password': 'password1'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json)

    def test_login_invalid(self):
        response = self.client.post('/login', json={'username': 'user1', 'password': 'wrong_password'})
        self.assertEqual(response.status_code, 401)

    def test_generate_array_authenticated(self):
        token = jwt.encode({'username': 'user1', 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        headers = {'Authorization': 'Bearer ' + token}
        response = self.client.post('/generate_array', json={'sentence': 'Authenticated test'}, headers=headers)
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertTrue(isinstance(data, list))
        self.assertEqual(len(data), 500)

    def test_generate_array_unauthenticated(self):
        response = self.client.post('/generate_array', json={'sentence': 'Unauthenticated test'})
        self.assertEqual(response.status_code, 401)


    def test_monitoring(self):
        token = jwt.encode({'username': 'user1', 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        headers = {'Authorization': 'Bearer ' + token}
        response = self.client.post('/generate_array', json={'sentence': 'Test'}, headers=headers)
        data = response.json
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 500)


if __name__ == '__main__':
    import unittest
    unittest.main()
