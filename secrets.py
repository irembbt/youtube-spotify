from os import getenv


def get_spotify_credentials():
    username = getenv("SPOTIFY_USERNAME")
    token = getenv("SPOTIFY_OAUTH_TOKEN")

    return username, token
