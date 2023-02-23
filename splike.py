#!/usr/local/bin/python3

import sys
import argparse
import spotipy
from spotipy.oauth2 import SpotifyOAuth
# from termcolor import colored

arg_parser=argparse.ArgumentParser(prog='splike')
sub_parsers=arg_parser.add_subparsers()

def authSpotify():
    scope="user-read-playback-state user-modify-playback-state user-library-modify"
    return spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

def printInfo(device, track):
    track_id=track['item']['id']
    artists=parseArtists(track)

    print("Now playing: {0} - {1}\nOn {3}: {2}"
          .format(artists,
                  track['item']['name'],
                  device['name'],
                  device['type']))

def addToLibrary(args):
    session=authSpotify()
    device=getActiveDevice(session)
    track=session.current_user_playing_track()
    printInfo(device, track)
    try:
        track_id=track['item']['id']
        session.current_user_saved_tracks_add(tracks=[track_id])
        print("Added to My Library!")
    except:
        print("Something went wrong while adding track to My Library")

def removeFromLibrary(args):
    session=authSpotify()
    device=getActiveDevice(session)
    track=session.current_user_playing_track()
    printInfo(device, track)
    try:
        track_id=track['item']['id']
        session.current_user_saved_tracks_delete(tracks=[track_id])
        print("Removed from My Library!")
    except:
        print("Something went wrong while removing track from My Library")

def parseArtists(track):
    artists=[]
    for artist in track['item']['artists']:
        artists.append(artist['name'])
    return ', '.join(artists)

def getActiveDevice(session):
    for device in session.devices()['devices']:
        if device['is_active']:
            return device


like_parser=sub_parsers.add_parser('like')
like_parser.set_defaults(func=addToLibrary)
dislike_parser=sub_parsers.add_parser('unlike', aliases=['dislike', 'remove'])
dislike_parser.set_defaults(func=removeFromLibrary)

if __name__ == "__main__":
    args = arg_parser.parse_args()
    args.func(args)
