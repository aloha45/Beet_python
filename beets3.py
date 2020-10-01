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

turn = 1
count = 0
board = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
game_won  = False
player = 'X'

def print_divider():
    print("-------------")
    
def print_board(board):
    print(" " + board[6] + " " + "|" + " " + board[7] + " " + "|" + " " + board[8])
    print_divider()
    print(" " + board[3] + " " + "|" + " " + board[4] + " " + "|" + " " + board[5])
    print_divider()
    print(" " + board[0] + " " + "|" + " " + board[1] + " " + "|" + " " + board[2])

def win_game():
    global player, board, game_won

    hor1 = [board[0], board[1], board[2]]
    hor2 = [board[3], board[4], board[5]]
    hor3 = [board[6], board[7], board[8]]
    diag1 = [board[0], board[4], board[8]]
    diag2 = [board[6], board[4], board[2]]
    ver1 = [board[0], board[3], board[6]]
    ver2 = [board[1], board[4], board[7]]
    ver3 = [board[2], board[5], board[8]]
    
    win_conditions = [hor1, hor2, hor3, diag1, diag2, ver1, ver2, ver3]
    print(hor1)
    for win in win_conditions:
        if win.count('X') == 3:
            game_won = True
            print(f'congrats {player} you win')
        elif win.count('O') == 3:
            game_won = True
            print(f'congrats {player} you win')
    get_move()

def get_move():
    global game_won
    while game_won == False:
        move()
        print_board(board)
        turn_switcher()
        win_game()
    
def turn_switcher():
    global turn, player
    turn *= -1
    if turn == 1:
        player = 'X'
    if turn == -1:
        player = 'O'

def move():
    global count, board, turn, player
    player_move = int(input('Please enter a square: '))
    if board[player_move-1] == 'X' or board[player_move-1] =='O':
        get_move()
    board[player_move-1] = player
    count += 1

def game():
    print_board(board)
    get_move()

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
# print(json.dumps(user, sort_keys=True, indent=4))
# print(user_devices)
device_id = (user_devices['devices'][0]['id'])
# print(device_id)
choice = ''

displayName = user['display_name']
followers = user['followers']['total']

print(displayName)

choices = ['0 - Exit', '1 - Search by Artist', '2 - Search by Album', '3 - Search by Song', '4 - Play Pic-Pax']

while True:
    print()
    print('Please enter a choice between 0 and 4: ')
    print('>>> Welcome to Beets 3.0 ' + displayName + '!')
    print('>>> You have ' + str(followers) + ' followers.')
    print()
    for num in choices:
        print(num)
    print()
    choice = int(input('Your choice: '))

    if choice > 4:
        print()
        print('Invalid response. Please enter a choice between 0 and 4: ')
        for num in choices:
            print(num)
        print()
        choice = int(input('Your choice: '))


    #End the program
    if choice == 0:
        break

    #Search for an artist
    if choice == 1:
        search_query_artist = input('Enter artist name: ')
        results_artist = input('How many results would you like? ')
        print()

        # Get search results
        search_results_artist = spotifyObject.search(search_query_artist, results_artist, 0, 'artist')
        print(json.dumps(search_results_artist, sort_keys=True, indent=4))

        artist = search_results_artist['artists']['items'][0]
        artist_art = artist['images'][0]['url']
        webbrowser.open(artist_art)
        artist_id = artist['id']
        print(artist['name'])
        artist_uri = artist['uri']
        
        top_tracks_artist = spotifyObject.artist_top_tracks(artist_id, country='US')
        top_track_uri = top_tracks_artist['tracks'][1]['album']['uri']

        spotifyObject.start_playback(context_uri=top_track_uri, offset=None)

    if choice == 2:
        search_query = input('Enter album name: ')
        results_album = input('How many results would you like? ')
        print()

        # Get search results
        search_results_album = spotifyObject.search(search_query, results_album, 0, 'album')
        print(json.dumps(search_results_album, sort_keys=True, indent=4))
        album_art = search_results_album['albums']['items'][0]['images'][0]['url']
        album_uri = search_results_album['albums']['items'][0]['uri']

        webbrowser.open(album_art)
        spotifyObject.start_playback(context_uri=album_uri, offset=None)
    
    if choice == 3:
        search_query_track = input('Enter song name: ')
        results_track = input('How many results would you like? ')
        print()

        # Get search results
        search_results_track = spotifyObject.search(search_query_track, results_track, 0, 'track')
        print(json.dumps(search_results_track, sort_keys=True, indent=4))
        track_uri = search_results_track['tracks']['items'][0]['album']['uri']
        # print(track_uri)

        spotifyObject.start_playback(context_uri=track_uri, offset=None)

    if choice == 4:
        game()
        
