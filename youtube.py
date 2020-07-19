import os
import pickle
import requests
import youtube_dl

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from pprint import pprint


class YoutubeVideos:
    def __init__(self, client_secrets_filename):
        self.youtube_client = self.get_youtube_client(client_secrets_filename)
        self.all_song_info = {}

        request = self.youtube_client.channels().list(
            part="snippet,contentDetails,statistics", mine=True
        )
        channel_list = request.execute()
        my_channel = channel_list["items"][0]

        self.liked_pid = my_channel["contentDetails"]["relatedPlaylists"]["likes"]

    def get_youtube_client(self, client_secrets_filename):
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
        api_service_name = "youtube"
        api_version = "v3"

        cache_name = "youtube_credentials.pickle"

        creds = None
        if os.path.exists(cache_name):
            with open(cache_name, "rb") as f:
                creds = pickle.load(f)

        if (
            not creds or not creds.valid
        ):  # creds.valid checks if stored auth token can be used as is.
            if creds and creds.expired and creds.refresh_token:
                # creds.expired checks if auth token needs to be refreshed.
                creds.refresh(Request())
            else:
                # Get credentials and create an API client
                flow = InstalledAppFlow.from_client_secrets_file(
                    client_secrets_filename, scopes
                )
                creds = flow.run_local_server(port=0)

            with open(cache_name, "wb") as f:
                pickle.dump(creds, f)

        # from the Youtube DATA API
        youtube_client = build(api_service_name, api_version, credentials=creds)

        return youtube_client

    def get_liked_videos(self):

        vids = list()

        for item in self._get_set_of_videos():
            video_title = item["snippet"]["title"]
            item_id = item["contentDetails"]["videoId"]
            youtube_url = f"https://www.youtube.com/watch?v={item_id}"
            print(video_title)
            vid_items = self._process_vid(youtube_url, video_title)
            if vid_items:
                vids.append(vid_items)

        return vids

    def _get_set_of_videos(self):
        vids = list()

        # Grab Our Liked Videos & Create A Dictionary Of Important Song Information
        request = self.youtube_client.playlistItems().list(
            part="snippet,contentDetails,id", playlistId=self.liked_pid
        )
        response = request.execute()

        # Get first set of videos
        vid_items = response["items"]
        # vids.extend(vid_items)

        for item in vid_items:
            yield item

        # Keep getting other videos
        while "nextPageToken" in response:
            response = (
                self.youtube_client.playlistItems()
                .list(
                    part="snippet,contentDetails,id",
                    pageToken=response["nextPageToken"],
                    playlistId=self.liked_pid,
                )
                .execute()
            )
            vid_items = response["items"]
            # vids.extend(vid_items)

            for item in vid_items:
                yield item

        # return vids

    def _process_vid(self, youtube_url, video_title):
        # use youtube_dl to collect the song name & artist name
        video = youtube_dl.YoutubeDL({}).extract_info(youtube_url, download=False)
        song_name = video["track"]
        artist = video["artist"]

        if song_name is not None and artist is not None:
            # save all important info and skip any missing song and artist
            self.all_song_info[video_title] = {
                "youtube_url": youtube_url,
                "song_name": song_name,
                "artist": artist,
            }
            return song_name, artist
