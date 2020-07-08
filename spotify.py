import json
import requests
from os import getenv

import spotipy
from spotipy.oauth2 import SpotifyOAuth


class SpotifySongs:
    def __init__(self):
        scope = " ".join(
            [
                "playlist-modify-private",
                "playlist-read-private",
                "playlist-read-collaborative",
            ]
        )
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
        self.user_id = "irembulut"

    def _create_playlist(self, name):
        response = self.sp.user_playlist_create(
            self.user_id, name, public=False, description="Youtube Liked Videos",
        )
        id = response["id"]
        return id

    def _check_playlist_exists(self, name):
        playlists = self.sp.user_playlists(self.user_id)
        for playlist in playlists["items"]:
            if playlist["name"] == name and playlist["owner"]["id"] == self.user_id:
                return playlist["id"]

    def get_or_create_playlist(self, name):
        id = self._check_playlist_exists(name)
        if id is None:
            print("Creating playlist")
            return self._create_playlist(name)
        else:
            print("Playlist exists")
            return id

    def get_spotify_uri(self, song_name, artist):
        # Search for the song
        songname = song_name
        songartist = artist

        query = f'track:{songname} artist:"{songartist}"'
        response = self.sp.search(q=query, type="track", limit=5, offset=0)
        songs = response["tracks"]["items"]

        # only use the first song
        uri = songs[0]["uri"]

        return uri

    def add_song_to_playlist(self, uri_list, id):

        check_uri_exist = self.sp.playlist_tracks(id, fields="items(track(uri))")
        existing_uri_song_set = {
            track["track"]["uri"]
            for track in check_uri_exist["items"]  # set comprehension
        }

        # existing_uri_song_list = list()
        # for track in check_uri_exist["items"]:
        # existing_uri_song_list.append(track["track"]["uri"])

        for uri in uri_list:
            if uri not in existing_uri_song_set:
                self.sp.user_playlist_add_tracks(self.user_id, id, [uri])
                print(f"added song {uri}")
            else:
                print(f"song {uri} already exists")

        # print(check_uri_exist)
        # print(existing_uri_song_set)

    def add_songs_to_spotify(self, vids, id):
        uri_list = [self.get_spotify_uri(name, artist) for name, artist in vids]
        self.add_song_to_playlist(uri_list, id)

        # uri_list = list()
        # for name, artist in vids:
        #     uri_list.append(self.get_spotify_uri(name, artist))
