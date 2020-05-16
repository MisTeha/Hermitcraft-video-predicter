from Hermits import HermitIDs
from googleapiclient.discovery import build
import json

APIKEY = "AIzaSyCWgnwSZxKK4ayoX8_0OJEK83gOtDmpRns"
youtube = build('youtube', 'v3', developerKey=APIKEY)

def getChannelVideos(channelId):
    videos = []
    nextPageToken = None
    

    try: 
        result = youtube.channels().list(id=channelId, part='contentDetails').execute()
        uploadsPL = result['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    except KeyError as e:
        print(result)
        raise e

    result = youtube.playlistItems().list(playlistId=uploadsPL, part='snippet', maxResults=21).execute()
    videos += result['items']
    nextPageToken = result.get('nextPageToken')
    
    return videos

data = {}
videoitems = {}
with open("results.json", 'w') as file:
    for hermit in HermitIDs:
        data[hermit.name] = []
        videoitems[hermit.name] = []
        videos = getChannelVideos(hermit)
        videoitems[hermit.name].append(videos)
        print(f"Appended videos for {hermit.name}")
        for i, video in enumerate(videos):
            data[str(hermit.name)].append({
                str(i): video['snippet']['title']
            })
            print(f"Wrote video {i} for {hermit.name}")
    indent = 2
    json.dump(data, file, indent = 1, sort_keys=True)
with open("videoitems.json", 'w') as file:
    json.dump(videoitems, file, indent = 1, sort_keys=True)
print("DONE")