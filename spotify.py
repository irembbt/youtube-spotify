import json
import secrets
import requests

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

    def get_spotify_uri(self):
        pass

    def add_song_to_playlist(self):
        pass
