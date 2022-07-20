from flask import Flask, request, jsonify, make_response
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
import uuid
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps





app = Flask(__name__)

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

db = SQLAlchemy(app)

# Register a user
# - Login a user
# - List all users
# - User can create a post
# - User can list own posts
# - User can not view other users posts
# - User can edit or delete own posts
# - Use JWT token
# - Add pagination on users and posts

# Document code
# Have unit tests



# Endpoints:
# POST /v1/user/register
# INPUT: {name: ‘Full Name’, phone_number: ‘777777’, password: ‘**’, repeat_password: ‘**’}
# OUTPUT: {status: 200, message: ‘User has been registered’}


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"User('{self.name}', '{self.phone_number}')"

class Post(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('posts', lazy=True))

    def __repr__(self):
        return f"Post('{self.title}', '{self.description}')"

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(id=data['id']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

@app.route('/v1/user/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(name=data['name'], phone_number=data['phone_number'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'status': 200, 'message': 'User has been registered'})

# POST /v1/user/login
# INPUT: {phone_number: ‘777777’, password: ‘******’}
# OUTPUT: {status: 200, message: ‘User logged in successfully’, user: {name: ‘Full Name’, phone_number: "777777"}}

@app.route('/v1/user/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(phone_number=data['phone_number']).first()
    if not user:
        return jsonify({'status': 404, 'error': 'User not found'})
    if check_password_hash(user.password, data['password']):
        token = jwt.encode({'user_id': user.id, 'exp': '3600'}, app.config['SECRET_KEY'])
        return jsonify({'status': 200, 'message': 'User logged in successfully', 'user': {'name': user.name, 'phone_number': user.phone_number, 'token': token}})
    else:
        return jsonify({'status': 404, 'error': 'Wrong password'})

# GET /v1/users?page=1&users=25
# OUTPUT: {status: 200, users: [{name: ‘Full Name’, phone_number: "6666"},{name: ‘Full Name’, phone_number: "5555"}, ...]}

@app.route('/v1/users', methods=['GET'])
def get_users():
    page = request.args.get('page', 1, type=int)
    users = User.query.paginate(page, 25, False)
    return jsonify({'status': 200, 'users': [{'name': user.name, 'phone_number': user.phone_number} for user in users.items]})

# POST /v1/new/post
# INPUT: {title: ‘Post title’, description: ‘description’}
# OUTPUT: {status: 200, message: ‘Post has been created’, post: {id: ‘fscsd’}}

@app.route('/v1/new/post', methods=['POST'])
@token_required
def new_post():
    data = request.get_json()
    new_post = Post(title=data['title'], description=data['description'], user_id=data['user_id'])
    db.session.add(new_post)
    db.session.commit()
    return jsonify({
        'status': 200, 
        'message': 'Post has been created', 
        'post': {
            'id': new_post.id, 
            'title': new_post.title, 
            'description': new_post.description
        }})


# GET /v1/posts?page=1&posts=25
# OUTPUT: {status: 200, posts: [{title: ‘Full Name’, description: "sdfsfs"},{title: ‘Full Name’, description: "sfsfsdf"}, ...]}
@app.route('/v1/posts', methods=['GET'])
@token_required
def get_posts():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.paginate(page, 25, False)
    return jsonify({'status': 200, 'posts': [{'id': post.id, 'title': post.title, 'description': post.description} for post in posts.items]})


# PATCH /v1/posts/:id
# INPUT: {id: ‘fsfsd’, title: ‘Post title’, description: ‘description’}
# OUTPUT: {status: 200, message: ‘Post has been updated’, post: {id: ‘fscsd’}}
@app.route('/v1/posts/<id>', methods=['PATCH'])
@token_required
def update_post(id):
    data = request.get_json()
    post = Post.query.filter_by(id=id).first()
    if not post:
        return jsonify({'status': 404, 'error': 'Post not found'})
    post.title = data['title']
    post.description = data['description']
    db.session.commit()
    return jsonify({'status': 200, 'message': 'Post has been updated', 'post': {'id': post.id, 'title': post.title, 'description': post.description}})

# GET /v1/posts/:id
# INPUT: {id: ‘fsfsd’}
# OUTPUT: {status: 200, post: {id: ‘fscsd’, title: ‘Post title’, description: ‘description’}}

@app.route('/v1/posts/<id>', methods=['GET'])
@token_required
def get_post(id):
    post = Post.query.filter_by(id=id).first()
    if not post:
        return jsonify({'status': 404, 'error': 'Post not found'})
    return jsonify({'status': 200, 'post': {'id': post.id, 'title': post.title, 'description': post.description}})

# DELETE /v1/posts/:id
# INPUT: {id: ‘fsfsd’}
# OUTPUT: {status: 200, message: ‘Post has been deleted}
@app.route('/v1/posts/<id>', methods=['DELETE'])
@token_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()
    if not post:
        return jsonify({'status': 404, 'error': 'Post not found'})
    db.session.delete(post)
    db.session.commit()
    return jsonify({'status': 200, 'message': 'Post has been deleted'})





if __name__ == '__main__':
    app.run(debug=True)
