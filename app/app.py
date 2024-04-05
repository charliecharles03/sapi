from flask import Flask
from flask_cors import CORS
from .resources.auth.userAPI import UserAPI , LoginAPI, Register

from .resources.auth.songsAPI import Get_songs_route,  Add_song_route
from flask_jwt_extended import JWTManager

from .models.model import create_tables

import os

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'bro-code' # Change this!
app.config['SECRET_KEY'] = 'super-secret'  # Change this!

jwt = JWTManager(app)

CORS(app)
CORS(
    app,
    resources={
        r"/*": {
            "origins": "http://localhost:5173",
            "supports_credentials": True,
            "Access-Control-Allow-Credentials": True,
        }
    },
)



@app.route('/')
def index():
    return 'Hello, world!'


app.add_url_rule('/api/auth/userprofile/', view_func=UserAPI.as_view('user_profile'),methods=['GET'])

app.add_url_rule('/api/auth/login', view_func=LoginAPI.as_view('login_api'), methods=['POST'])

app.add_url_rule('/api/auth/recents', view_func=Get_songs_route, methods=['GET'])

app.add_url_rule('/api/auth/addsong', view_func=Add_song_route, methods=['POST'])


#songs end points

app.add_url_rule('/api/auth/songs', view_func=Register, methods=['POST'])


if __name__ == '__main__':
    app.run(debug=True)

