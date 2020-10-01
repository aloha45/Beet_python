import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError

os.environ['SPOTIPY_CLIENT_ID']='929032b8613349b68ccf481619c25fa6'
os.environ['SPOTIPY_CLIENT_SECRET']='75089110568743bebc5e4bb68b033bbd'
os.environ['SPOTIPY_REDIRECT_URI']='http://google.com/'

# Get username from terminal

username = sys.argv[1]
# 1297289791

scope = 'user-read-private user-read-playback-state user-modify-playback-state'

# Erase cache and prompt for user permission
try:
    token = util.prompt_for_user_token(username, scope)
except:
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username, scope)

spotifyObject = spotipy.Spotify(auth=token)

user = spotifyObject.current_user()
user_devices = spotifyObject.devices()
print(json.dumps(user, sort_keys=True, indent=4))
print(user_devices)
device_id = (user_devices['devices'][0]['id'])
print(device_id)

displayName = user['display_name']
followers = user['followers']['total']

print(displayName)

while True:
    print()
    print('>>> Welcome to Beets 3.0 ' + displayName + '!')
    print('>>> You have ' + str(followers) + ' followers.')
    print('0 - Exit')
    print('1 - Search by Artist')
    print('2 - Search by Song')
    print('3 - Search by Album')
    print()
    choice = input('Your choice: ')

    #End the program
    if choice == '0':
        break

    #Search for an artist
    if choice == '1':
        search_query_artist = input('Enter artist name: ')
        results_artist = input('How many results would you like? ')
        print()

        # Get search results
        search_results_artist = spotifyObject.search(search_query_artist, results_artist, 0, 'artist')
        print(json.dumps(search_results_artist, sort_keys=True, indent=4))

        artist = search_results_artist['artists']['items'][0]
        webbrowser.open(artist['images'][0]['url'])
        artist_id = artist['id']
        print(artist['name'])
        artist_uri = artist['uri']
        print(artist_uri)
        
        top_tracks_artist = spotifyObject.artist_top_tracks(artist_id, country='US')
        top_track_uri= top_tracks_artist['tracks'][1]['album']['uri']

        spotifyObject.start_playback(context_uri=top_track_uri, offset=None)
    
    if choice == '2':
        search_query_track = input('Enter song name: ')
        results_track = input('How many results would you like? ')
        print()

        # Get search results
        search_results_track = spotifyObject.search(search_query_track, results_track, 0, 'track')
        print(json.dumps(search_results_track, sort_keys=True, indent=4))
    
    if choice == '3':
        search_query = input('Enter album name: ')
        results_album = input('How many results would you like? ')
        print()

        # Get search results
        search_results_album = spotifyObject.search(search_query, results_album, 0, 'album')
        print(json.dumps(search_results_album, sort_keys=True, indent=4))

        
