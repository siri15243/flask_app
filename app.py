from flask import Flask, request, jsonify
import logging
from random import SystemRandom
from flask_limiter import Limiter
from flask_testing import TestCase
from dotenv import load_dotenv
import jwt
import datetime
from functools import wraps
import yaml
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_FILE_PATH = os.path.join(BASE_DIR, 'users_db', 'users.yaml')

app = Flask(__name__)
load_dotenv()

secret_key = os.environ.get('SECRET_KEY')
app.config['SECRET_KEY'] = secret_key

random_gen = SystemRandom()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PORT = os.environ.get('PORT')


def load_user_details():
    with open(USERS_FILE_PATH, 'r') as file:
        return yaml.safe_load(file)['users']

users = load_user_details()


limiter = Limiter(
    app,
    default_limits=["10 per minute"]
)


def requires_jwt(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            decoded_token = jwt.decode(token.split()[1], app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = decoded_token['username']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401

        return func(current_user, *args, **kwargs)
    return decorated



def update_user_details(updated_users):
    data = {'users': updated_users}
    with open('users_db/users.yaml', 'w') as file:
        yaml.dump(data, file)

@app.route('/health', methods=['GET'])
def health():
    return 'health-ok'

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if username in users:
        return jsonify({'message':'User registered already, Please login'})
    
    else :
        users[username] = password
        update_user_details(users)
        return jsonify({'message': 'User registered successfully'})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if username in users and users[username] == password:
        token = jwt.encode({'username': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token':token})
    else:
        logger.info(f"Error:Authentication Failed")
        return jsonify({'message': 'Authentication failed'}), 401




@app.route('/generate_array', methods=['POST'])
@requires_jwt
@limiter.limit("10 per minute")  
def generate_array(current_user):
    """
    Generate a random 500-dimensional array of floats.

    Input: JSON object containing a 'sentence' key.
    Output: JSON array containing the random float array.

    Example Input: {"sentence": "This is a sample sentence"}
    Example Output: [0.123, 0.456, ...]

    :return: JSON response
    """
    try:
        input_sentence = request.json['sentence']
        random_array = [random_gen.uniform(0, 1) for _ in range(500)]
        logger.info(f"Generated array for input: {input_sentence}")
        return jsonify(random_array)
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 400


class TestAPI(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_valid_input(self):
        response = self.client.post('/generate_array', json={'sentence': 'Test'})
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertTrue(isinstance(data, list))
        self.assertEqual(len(data), 500)

    def test_invalid_input(self):
        response = self.client.post('/generate_array', json={'invalid_key': 'Test'})
        self.assertEqual(response.status_code, 400)

    def test_register(self):
        response = self.client.post('/register', json={'username': 'new_user', 'password': 'new_password'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'User registered successfully'})

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

if __name__ == '__main__':
    app.run(debug=True,port=PORT)
