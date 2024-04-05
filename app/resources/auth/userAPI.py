from flask import request, jsonify, session
from flask.views import MethodView
from flask_restful import Resource
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

from ...models.model import register_user, authenticate_user


# Sample user data (for a music app)

users = {
    1: {
        "user_id": 1,
        "username": "musiclover92",
        "email": "musiclover92@example.com",
        "full_name": "Alice Smith",
        "date_of_birth": "1992-05-15",
        "role_type": "user",  # Example role type
        "favorite_genres": ["pop", "rock", "hip hop"],
        "playlists": {
            "favorites": [1, 2, 3],
            "party_mix": [4, 5, 6]
        }
    },
    2: {
        "user_id": 2,
        "username": "jazzmaster",
        "email": "jazzmaster@example.com",
        "full_name": "Bob Johnson",
        "date_of_birth": "1985-09-20",
        "role_type": "admin",  # Example role type
        "favorite_genres": ["jazz", "blues"],
        "playlists": {
            "favorites": [7, 8, 9]
        }
    },
    # Add more users as needed
}


class UserAPI(MethodView):
    def get(self):
        user_id = request.args.get('user_id')
        user = users.get(int(user_id))
        if user:
            return jsonify(user), 200
        else:
            return jsonify({"error": "User not found"}), 404



def Register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        email = request.form['email']
        if register_user(username, password, role,email) == True:
            return 'User registered successfully!'
        else:
            return 'Username already exists!'


class LoginAPI(Resource):
    def post(self):
        username = request.json.get('username', None)
        password = request.json.get('password', None)
        user = authenticate_user(username, password)
        user_item = {
            "user_id": user[0],
            "username": user[1],
            "email": user[4],
            "role_type": user[3],
        }
        # Add your authentication logic here (e.g., validate username and password)
        if user:
            session['username'] = user[1]
            session['role'] = user[3]
            access_token = create_access_token(identity=username)
            response = {'users': user_item, 'access_token': access_token}
            return jsonify(response),200
        else:
            return jsonify({"error": "Invalid username or password"}), 401
