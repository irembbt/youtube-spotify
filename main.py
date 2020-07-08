import spotify, youtube
from pprint import pprint


def main():
    spofi = spotify.SpotifySongs()
    playlist_id = spofi.get_or_create_playlist("Youtube Liked Vids")

    youtube_client = youtube.YoutubeVideos("client_secret.json")
    youtube_songs = youtube_client.get_liked_videos()

    spofi_songs = spofi.add_songs_to_spotify(youtube_songs, playlist_id)


if __name__ == "__main__":
    main()
