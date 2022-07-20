# Create unit test for the following:
# GET /v1/posts/:id
# INPUT: {id: ‘fsfsd’}
# OUTPUT: {status: 200, post: {id: ‘fscsd’, title: ‘Post title’, description: ‘description’}}
import unittest
from main import app
import json
from main import db

TEST_DB = 'test.db'
BASE_URL = 'http://localhost:5000'

# Endpoints:
# POST /v1/user/register
# INPUT: {name: ‘Full Name’, phone_number: ‘777777’, password: ‘**’, repeat_password: ‘**’}
# OUTPUT: {status: 200, message: ‘User has been registered’}


# POST /v1/user/login
# INPUT: {phone_number: ‘777777’, password: ‘******’}
# OUTPUT: {status: 200, message: ‘User logged in successfully’, user: {name: ‘Full Name’, phone_number: "777777"}}



# GET /v1/users?page=1&users=25
# OUTPUT: {status: 200, users: [{name: ‘Full Name’, phone_number: "6666"},{name: ‘Full Name’, phone_number: "5555"}, ...]}


# POST /v1/new/post
# INPUT: {title: ‘Post title’, description: ‘description’}
# OUTPUT: {status: 200, message: ‘Post has been created’, post: {id: ‘fscsd’}}


# PATCH /v1/posts/:id
# INPUT: {id: ‘fsfsd’, title: ‘Post title’, description: ‘description’}
# OUTPUT: {status: 200, message: ‘Post has been updated’, post: {id: ‘fscsd’}}

# GET /v1/posts?page=1&posts=25
# OUTPUT: {status: 200, posts: [{title: ‘Full Name’, description: "sdfsfs"},{title: ‘Full Name’, description: "sfsfsdf"}, ...]}


# GET /v1/posts/:id
# INPUT: {id: ‘fsfsd’}
# OUTPUT: {status: 200, post: {id: ‘fscsd’, title: ‘Post title’, description: ‘description’}}


# DELETE /v1/posts/:id
# INPUT: {id: ‘fsfsd’}
# OUTPUT: {status: 200, message: ‘Post has been deleted}

# ON ERROR
# {status: 404, error: "There is no task at that id"}

class TestBase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + TEST_DB
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.drop_all()

    def test_register(self):
        # Register a new user
        data = {'name': 'Full Name', 'phone_number': '0787887455', 'password': 'platinum', 'repeat_password': 'platinum'}
        response = self.app.post(BASE_URL + '/v1/user/register', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'User has been registered')

    def test_login(self):
        # Register a new user
        data = {'phone_number': '0787887455', 'password': 'platinum'}
        response = self.app.post(BASE_URL + '/v1/user/register', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'User has been registered')
        # Login a user
        data = {'phone_number': '0787887455', 'password': 'platinum'}
        response = self.app.post(BASE_URL + '/v1/user/login', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'User logged in successfully')

    def test_get_users(self):
        # Register a new user
        data = {'name': 'Full Name', 'phone_number': '0787887455', 'password': 'platinum', 'repeat_password': 'platinum'}
        response = self.app.post(BASE_URL + '/v1/user/register', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'User has been registered')

        # Get all users
        response = self.app.get(BASE_URL + '/v1/users?page=1&users=25')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['users'][0]['name'], 'Full Name')
        self.assertEqual(response.json['users'][0]['phone_number'], '0787887455')
    
    def test_new_post(self):
        # Register a new user
        data = {'name': 'Full Name', 'phone_number': '0787887455', 'password': 'platinum', 'repeat_password': 'platinum'}
        response = self.app.post(BASE_URL + '/v1/user/register', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'User has been registered')
        # Login a user
        data = {'phone_number': '0787887455', 'password': 'platinum'}
        response = self.app.post(BASE_URL + '/v1/user/login', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'User logged in successfully')
        # Create a new post
        data = {'title': 'Post title', 'description': 'description'}
        response = self.app.post(BASE_URL + '/v1/new/post', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Post has been created')
        self.assertEqual(response.json['post']['title'], 'Post title')
        self.assertEqual(response.json['post']['description'], 'description')


    def test_update_post(self):
        # Register a new user
        data = {'name': 'Full Name', 'phone_number': '0787887455', 'password': 'platinum', 'repeat_password': 'platinum'}
        response = self.app.post(BASE_URL + '/v1/user/register', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'User has been registered')
        # Login a user
        data = {'phone_number': '0787887455', 'password': 'platinum'}
        response = self.app.post(BASE_URL + '/v1/user/login', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'User logged in successfully')
        # Create a new post
        data = {'title': 'Post title', 'description': 'description'}
        response = self.app.post(BASE_URL + '/v1/new/post', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Post has been created')
        self.assertEqual(response.json['post']['title'], 'Post title')
        self.assertEqual(response.json['post']['description'], 'description')
        # Update a post
        data = {'id': response.json['post']['id'], 'title': 'Post title', 'description': 'description'}
        response = self.app.patch(BASE_URL + '/v1/posts/' + response.json['post']['id'], data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'],'Post has been updated')
        self.assertEqual(response.json['post']['title'], 'Post title')
        self.assertEqual(response.json['post']['description'], 'description')


    def test_delete_post(self):
        # Register a new user
        data = {'name': 'Full Name', 'phone_number': '0787887455', 'password': 'platinum', 'repeat_password': 'platinum'}
        response = self.app.post(BASE_URL + '/v1/user/register', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'User has been registered')
        # Login a user
        data = {'phone_number': '0787887455', 'password': 'platinum'}
        response = self.app.post(BASE_URL + '/v1/user/login', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'User logged in successfully')
        # Create a new post
        data = {'title': 'Post title', 'description': 'description'}
        response = self.app.post(BASE_URL + '/v1/new/post', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Post has been created')
        self.assertEqual(response.json['post']['title'], 'Post title')
        self.assertEqual(response.json['post']['description'], 'description')
        # Delete a post
        response = self.app.delete(BASE_URL + '/v1/posts/' + response.json['post']['id'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Post has been deleted')


    def test_get_post(self):
        # Register a new user
        data = {'name': 'Full Name', 'phone_number': '0787887455', 'password': 'platinum', 'repeat_password': 'platinum'}
        response = self.app.post(BASE_URL + '/v1/user/register', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'User has been registered')
        # Login a user
        data = {'phone_number': '0787887455', 'password': 'platinum'}
        response = self.app.post(BASE_URL + '/v1/user/login', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'User logged in successfully')
        # Create a new post
        data = {'title': 'Post title', 'description': 'description'}
        response = self.app.post(BASE_URL + '/v1/new/post', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Post has been created')
        self.assertEqual(response.json['post']['title'], 'Post title')
        self.assertEqual(response.json['post']['description'], 'description')
        # Get a post
        response = self.app.get(BASE_URL + '/v1/posts/' + response.json['post']['id'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Post has been retrieved')
        self.assertEqual(response.json['post']['title'], 'Post title')
        self.assertEqual(response.json['post']['description'], 'description')

    
if __name__ == "__main__":
    unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBase)
    unittest.TextTestRunner(verbosity=2).run(suite)
    
