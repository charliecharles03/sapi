from flask import request, jsonify
from flask.views import MethodView
from flask_restful import Resource

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

