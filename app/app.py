from flask import Flask
from flask_cors import CORS
from .resources.auth.userAPI import UserAPI , LoginAPI, Register
from .resources.auth.songsAPI import Get_songs_route,  Add_song_route, update_song_route, delete_song_route
from .resources.auth.playlistAPI import add_to_user_playlist,fetch_playlist, delete_from_user_playlist,get_Playlist_names_of_user
from .resources.auth.albumAPI import add_to_user_album, fetch_album, delete_album_by_name
from .resources.auth.adminStatsAPI import  stats_count, stats_album_count, stats_songs_count,stats_total
from flask_jwt_extended import JWTManager
from datetime import timedelta

from .models.model import create_tables

import os

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'bro-code' # Change this!
app.config['SECRET_KEY'] = 'super-secret'  # Change this!
app.config['JWT_ACESS_TOKEN_EXPIRES'] = timedelta(hours=10)

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
app.add_url_rule('/api/auth/register', view_func=Register, methods=['POST'])

#songs end points

app.add_url_rule('/api/auth/recents', view_func=Get_songs_route, methods=['GET'])
app.add_url_rule('/api/auth/addsong', view_func=Add_song_route, methods=['POST'])
app.add_url_rule('/api/auth/updatesong',view_func=update_song_route,methods=['POST'])
app.add_url_rule('/api/auth/deletesong',view_func= delete_song_route,methods=['DELETE'])


#playlist endpoints

app.add_url_rule('/api/auth/addplaylist',view_func=add_to_user_playlist,methods=["POST"])
app.add_url_rule('/api/auth/getplaylist',view_func=fetch_playlist,methods=["GET"])
app.add_url_rule('/api/auth/dplaylist',view_func=delete_from_user_playlist,methods=["DELETE"])
app.add_url_rule('/api/auth/userplaylist',view_func=get_Playlist_names_of_user,methods=["GET"])

#album endpoints

app.add_url_rule('/api/auth/addalbum',view_func=add_to_user_album,methods=["POST"])
app.add_url_rule('/api/auth/getalbum',view_func=fetch_album,methods=["GET"])
app.add_url_rule('/api/auth/deletealbumfull',view_func=delete_album_by_name,methods=["DELETE"])

#stats

app.add_url_rule('/api/auth/usercount',view_func=stats_count,methods=["GET"])
app.add_url_rule('/api/auth/albumcount',view_func=stats_album_count,methods=["GET"])
app.add_url_rule('/api/auth/songcount',view_func=stats_songs_count,methods=["GET"])
app.add_url_rule('/api/auth/totalcount',view_func=stats_total,methods=["GET"])

if __name__ == '__main__':
    app.run(debug=True)

