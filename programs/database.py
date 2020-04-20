from flask import Flask, render_template, request, jsonify
import json
import requests
access_token = 'BQBEor-q0Qsh_CT-qHMwl6-0VehPcTkb4uP4GI0eUauE76jwMpBeBA59F3jxsaxWhDc6Z2Lq4ST2_bD_Vf-zvUAf0R95xHmlPBrQ9RIyZLApUI9ABCyOjl3JLo1LxDed7ub7Pl10B-HnIkpP5D0HuQ5V_CYZIRAxM8KiXJSngZimV0AtjbPEXmAcGNAfEzCE25lBgXg4IaiSqPKIU_DUPkACbZMFCMI9iQVxPKzrgadbFsDrtlvcgqWMpW4hg5qs3-UDEqsU6ELzui0kk2LE9RLmQG32Ig'
f = open("spotify.csv","a")
artist_id = '0Onvkz1Nbs4wHXXUwOIGk8'
artists = 'https://api.spotify.com/v1/artists/'+ artist_id + '/albums?market=ES&limit=50&access_token=' + access_token
resp = requests.get(artists)
x = resp.json()
for i in x["items"]:
   for j in i["artists"]:
       artist = j["name"]
   song = i["name"]
   release_date = i["release_date"]
   total_tracks = i["total_tracks"]
   spotify_uri = i["uri"]
   record = artist + ',' + song + ',' + release_date + ',' + spotify_uri + '\n'
   f.write(record)
f.close()
