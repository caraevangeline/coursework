from flask import Flask, render_template, request, jsonify
import json
import requests
import requests_cache
import urllib.request
#from flask_restful import Resource
#requests_cache.install_cache('crime_api_cache', backend='sqlite', expire_after=36000)
app = Flask(__name__)
access_token = 'BQCW8FmZ5ofgu8Cjnh4xA-jLKbNrgWA4YzoPC68xw48lXll7a_NsbCCJSdILRvoMnWEym_ZRQSLutyszD3Xa6RrV4FPBXWFHZOVpmctEruecZWYjRihTGBHnJQc9X1SROV9gpe1DWggFw8btVInTnq5CeQ6FaBCO0roqBT2PeB6vYNPaUeOxlvT36yhTA5ckUKXXH5-ta1CJ8mJYgxnMOMT3wEvVbmJbE-dQbzMEkU99kli7zkJfD0utm_R8pgn2u-4-TwpYW4W0sfHC9gSLT_wbLvgv8A'

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
    if resp.ok:
       return jsonify(resp.json())
    else:
       print(resp.reason)

@app.route('/add_tracks/<playlist_id>', methods=["GET","POST"])
def add_tracks_f(playlist_id):
    #playlist_id = "1KfSKyY3wIXWzHSO0KfRiH"
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
       return 'Success'
    else:
       print(resp.reason)

@app.route('/unfollow_artist/<artist_id>', methods=["GET","DELETE"])                                                                                                                        @app.route('/unfollow_artist/<artist_id>', methods=["GET","DELETE"])
def unfollow_artist_f(artist_id):
    #artist_id = "3Nrfpe0tUJi4K4DXYWgMUX"
    unfollow_artist = 'https://api.spotify.com/v1/me/following?type=artist&ids=' + artist_id + '&access_token=' + access_token
    resp = requests.delete(url = unfollow_artist)
    if resp.ok:
       return 'Success'
    else:
       print(resp.reason)

if __name__=="__main__":
    app.run(host='0.0.0.0', ssl_context='adhoc')