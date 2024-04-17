from flask import Flask,jsonify,request
from ...models.model import get_playlist, add_to_playlist, delete_from_playlist,  get_playist_of_user, make_new_playlist

def add_to_user_playlist():
    data = request.json

    user_id = data.get('user_id')
    song_id = data.get('song_id')

    playlist_name = data.get('playlist_name')  # Add playlist_name parameter

    if user_id is None or song_id is None or playlist_name is None:
        return jsonify({"error": "user_id, song_id, and playlist_name are required"}), 400

    try:
        if add_to_playlist(user_id, song_id, playlist_name):
            return jsonify({"success": "Song added to playlist successfully"}), 201
        else:
            return jsonify({"error": "Failed to add song to playlist"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def fetch_playlist():
    user_id = request.args.get('user_id')

    if user_id is None:
        return jsonify({"error": "user_id is required"}), 400

    try:
        playlists =get_playlist(user_id)
        
        if not playlists:
            return jsonify({"error": "No playlists found"}), 404

        formatted_playlists = {}
        for row in playlists:
            playlist_name = row[0]
            song_data = row[1:]
            formatted_songs = []
            formatted_song = {
                "song_id": song_data[0],
                "title": song_data[1],
                "artist": song_data[2],
                "album": song_data[3],
                "duration": song_data[4],
                "genre": song_data[5],
                "year": song_data[6],
                "cover": song_data[7],
                "audio": song_data[8]
            }
            formatted_songs.append(formatted_song)
            
            if playlist_name in formatted_playlists:
                formatted_playlists[playlist_name].extend(formatted_songs)
            else:
                formatted_playlists[playlist_name] = formatted_songs

        return jsonify({"playlists": formatted_playlists}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def delete_from_user_playlist():
    data = request.json

    user_id = data.get('user_id')
    song_id = data.get('song_id')

    playlist_name = data.get('playlist_name')  # Add playlist_name parameter

    if user_id is None or song_id is None or playlist_name is None:
        return jsonify({"error": "user_id, song_id, and playlist_name are required"}), 400

    try:
        if delete_from_playlist(user_id, song_id, playlist_name):
            return jsonify({"success": "Song deleted from playlist successfully"}), 200
        else:
            return jsonify({"error": "Failed to delete song from playlist"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500



def  get_Playlist_names_of_user():
    user_id = request.args.get('user_id')
    if user_id is None:
        return jsonify({"error": "user_id is required"}), 400
    try:
        playlist_names =  get_playist_of_user(user_id)
        return jsonify(playlist_names),200
    except Exception as e:
        return jsonify({"error":str(e)}),500

def make_playlist():
    user_id = request.args.get('user_id')
    name = request.args.get('playlist_name')
    print(user_id)
    if user_id is None:
        return jsonify({"error": "user_id is required"}), 400
    try:
        make_new_playlist(user_id,name)
        return jsonify("successfully updated"),200
    except Exception as e:
        return jsonify({"error":str(e)}),500

