
from flask import Flask,jsonify,request
from ...models.model import  add_to_album ,get_album

def add_to_user_album():
    data = request.json

    user_id = data.get('user_id')
    song_id = data.get('song_id')
    album_name = data.get('album_name')  

    if user_id is None or song_id is None or album_name is None:
        return jsonify({"error": "user_id, song_id, and album_name are required"}), 400

    try:
        if add_to_album(user_id, song_id, album_name):
            return jsonify({"success": "Song added to album successfully"}), 201
        else:
            return jsonify({"error": "Failed to add song to album"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def fetch_album():
    user_id = request.args.get('user_id')

    if user_id is None:
        return jsonify({"error": "user_id is required"}), 400

    try:
        albums =get_album(user_id)
        
        if not albums:
            return jsonify({"error": "No albums found"}), 404

        formatted_albums = {}
        for row in albums:
            album_name = row[0]
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
            
            if album_name in formatted_albums:
                formatted_albums[album_name].extend(formatted_songs)
            else:
                formatted_albums[album_name] = formatted_songs

        return jsonify({"albums": formatted_albums}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


