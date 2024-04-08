from flask import Flask
from flask_cors import CORS
from .resources.auth.userAPI import UserAPI , LoginAPI, Register
from .resources.auth.songsAPI import Get_songs_route,  Add_song_route
from .resources.auth.playlistAPI import add_to_user_playlist,fetch_playlist, delete_from_user_playlist
from flask_jwt_extended import JWTManager
from datetime import timedelta

from .models.model import create_tables

import os

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'bro-code' # Change this!
app.config['SECRET_KEY'] = 'super-secret'  # Change this!
app.config['JWT_ACESS_TOKEN_EXPIRES'] = timedelta(hours=1)

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

#user enpoints
app.add_url_rule('/api/auth/userprofile/', view_func=UserAPI.as_view('user_profile'),methods=['GET'])
app.add_url_rule('/api/auth/login', view_func=LoginAPI.as_view('login_api'), methods=['POST'])

#songs end points

app.add_url_rule('/api/auth/recents', view_func=Get_songs_route, methods=['GET'])
app.add_url_rule('/api/auth/addsong', view_func=Add_song_route, methods=['POST'])
app.add_url_rule('/api/auth/songs', view_func=Register, methods=['POST'])


#playlist endpoints

app.add_url_rule('/api/auth/addplaylist',view_func=add_to_user_playlist,methods=["POST"])
app.add_url_rule('/api/auth/getplaylist',view_func=fetch_playlist,methods=["GET"])
app.add_url_rule('/api/auth/dplaylist',view_func=delete_from_user_playlist,methods=["DELETE"])

if __name__ == '__main__':
    app.run(debug=True)

