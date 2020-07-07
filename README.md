# Youtube To Spotify
A simple implementation of Youtube and Spotify connectors, to derive song videos listed under a users liked videos, and add them to a playlist in Spotify. 

# Possible extensions
- Abstract API calls with pagination into a simple generator.
- Add a pub-sub mechanism, in order to add other ideas concerning my liked videos with ease.
- A local cahce / database layer to weed out already processed liked videos. Currently, Youtube API delivers all liked videos.
- Deploy to AWS?? (With SNS taking over pub-sub mechanism)