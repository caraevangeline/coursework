from flask import Flask, request, jsonify, render_template
import requests
from cassandra.cluster import Cluster

cluster = Cluster(contact_points=['172.17.0.2'],port=9042)
session = cluster.connect()
app = Flask(__name__)

@app.route('/')
def hello():
    name = request.args.get("name","World")
    return('<h1>Hello, {}!</h1>'.format(name))

@app.route('/spotify_display/<song>')
def display(song):
    rows = session.execute( """Select * From spotify.statistics where song = '{}'""".format(song))
    for song1 in rows:
        return('<c><h1>{} is a part of {}!</h1></c>'.format(song,song1.artist))

    return 'Song does not exist!'

@app.route('/spotify_create',methods = ["GET","POST"])
def create():
    song = request.json.get('song', '')
    artist = request.json.get('artist', '')
    date = request.json.get('date', '')
    uri = request.json.get('uri', '')
    rows = session.execute( """Insert into spotify.statistics(song,artist,date,uri) values ('{}','{}','{}','{}')""".format(song,artist,date,uri))
    return 'Added Successfully'

@app.route('/spotify_delete/<song>',methods = ["GET","DELETE"])
def del_spotify(song):
    rows = session.execute( """Delete from spotify.statistics where song = '{}'""".format(song))
    return 'Deleted Successfully'

@app.route('/spotify_update/<artist>',methods = ["GET","PUT"])
def update_spotify(artist):
    rows = session.execute( """UPDATE spotify.statistics set artist= 'cara' where song = '{}'""".format(artist))
    return 'Updated Successfully'

access_token = 'BQDZFBVSHbt6ZzHwb0eGUOxQR7HHny58ZlXva3Bye2OtwWy9ux6jAONPV9rgAQpugO6ULQxOtHvRQ88fdPnKzem8ul3WmBEr_StztQDzF0h-EkXu0g9IITniJRqpHrAdzqqYEzy_QUKoVvosKZqrpE5UNtCz1I2MNZ0APxoLGADjrNCzw827UAi0BykhUljZNpibb-M1KgaX0pW8_8jJvF-Ywm_J4A6qK5Tj71ki2LV-uHb38wc2CqtDDK-pYK5zxdAmoovY6uXgvqfCK99T9uf2gHCIqA'

@app.route('/currently_playing', methods=['GET'])
def currently_playing_f():
    currently_playing = 'https://api.spotify.com/v1/me/player/currently-playing?access_token=' + access_token
    resp = requests.get(currently_playing)
    x = resp.json()
    if resp.ok:
       return render_template('currently_playing.html', result=x, mimetype='text/html')
       #return jsonify(resp.json())
    else:
        print(resp.reason)

@app.route('/cover_image/<play_id>', methods=['GET'])
def cover_image_f(play_id):
    #play_id = '3y35YGWmp1VVD8vsSOIR4D'
    cover_image = 'https://api.spotify.com/v1/playlists/' + play_id + '/images?access_token=' + access_token
    resp = requests.get(cover_image)
    x = resp.json()
    if resp.ok:
       return render_template('cover_image.html', result=resp.json(), mimetype='text/html')
       #return jsonify(resp.json())
    else:
       print(resp.reason)

@app.route('/recommendations', methods=['GET'])
def recommendations_f():
    recommendations = 'https://api.spotify.com/v1/recommendations/available-genre-seeds?access_token=' + access_token
    resp = requests.get(recommendations)
    if resp.ok:
       return render_template('recommendations.html', result=resp.json(), mimetype='text/html')
       #return jsonify(resp.json())
    else:
       print(resp.reason)

@app.route('/create_playlist/<user_id>', methods=["GET","POST"])
def create_playlist_f(user_id):
    #user_id = "dzg5zlif6tsiu0n5v9cnln2di"
    create_playlist = 'https://api.spotify.com/v1/users/' + user_id + '/playlists?access_token=' + access_token
    new_record = "{\"name\":\"Course Work\",\"description\":\"This playlist is created for the purpose of Cloud Computing Coursework\",\"public\":false}"
    resp = requests.post(url = create_playlist,data = new_record)
    if resp.ok:                                                                                                                                                                return jsonify(resp.json())
    else:
       print(resp.reason)

@app.route('/add_tracks/<playlist_id>', methods=["GET","POST"])
def add_tracks_f(playlist_id):
    #playlist_id = "4jx77EWucvBRyPY8eyseXo"
    track_id = "2elEVvWjPZltkotzcCwKvM"
    add_tracks = 'https://api.spotify.com/v1/playlists/' + playlist_id + '/tracks?uris=spotify%3Atrack%3A' + track_id + '&access_token=' + access_token
    resp = requests.post(url = add_tracks)
    if resp.ok:
       return jsonify(resp.json())
    else:
       print(resp.reason)

@app.route('/save_album/<album_id>', methods=["GET","PUT"])
def save_album_f(album_id):
    #album_id = "3n4DOUwVf6CSlW8zbjPGdW"
    save_album = 'https://api.spotify.com/v1/me/albums?ids=' + album_id +'&access_token=' + access_token
    resp = requests.put(url = save_album)
    if resp.ok:
       return 'Successfully saved an album'
    else:
       print(resp.reason)

@app.route('/unfollow_artist/<artist_id>', methods=["GET","DELETE"])
def unfollow_artist_f(artist_id):
    #artist_id = "3Nrfpe0tUJi4K4DXYWgMUX"
    unfollow_artist = 'https://api.spotify.com/v1/me/following?type=artist&ids=' + artist_id + '&access_token=' + access_token
    resp = requests.delete(url = unfollow_artist)
    if resp.ok:
       return 'The specified artist is unfollowed'
    else:
       print(resp.reason)


if __name__ == '__main__':
   app.run(host='0.0.0.0', port = 80)