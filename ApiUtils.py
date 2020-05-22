from googleapiclient.discovery import build
import datetime


APIKEY = "AIzaSyCWgnwSZxKK4ayoX8_0OJEK83gOtDmpRns"
youtube = build('youtube', 'v3', developerKey=APIKEY)

def datetimeToMillis(dt):
    return dt.timestamp() * 1000

class YTChannel:
    
    def __init__(self, channelId, keyword=""):
        self.channelId = channelId
        assert isinstance(keyword, str)
        self.keyword = keyword
        self.videos = self.getChannelVideos()
        self.latestVideo = self.getLatestVideo()
        
    #Returns the value of the uploads playlist id.
    def getUploadsPlaylist(self):
        return youtube.channels().list(id=self.channelId, part='contentDetails').execute()['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    

    #TODO: include "no video" exception. 
    #Returns a list of self's videos. Keyword being the filter, if given.
    def getChannelVideos(self, maxResults=39):
        assert isinstance(maxResults, int), "maxResults must be an integer"

        part = 'snippet'
        keyword = self.keyword
        pageToken = None
        videos = youtube.playlistItems().list(playlistId=self.getUploadsPlaylist(), part=part, maxResults=maxResults).execute()['items']
        return [video for video in videos if keyword in video['snippet']['title']]

        for i in range(5):
            result = youtube.playlistItems().list(playlistId=self.getUploadsPlaylist(), part=part, maxResults=maxResults).execute()
            pageToken = result.get('nextPageToken')
             

            if keyword in result['items'][0]['snippet']['title']:
                return result['items']
            elif pageToken is None:
                break
        raise Exception("No videos found")
            

    #TODO: merge this with getChannelVideos()
    #Returns the latest video. Keyword being the filter, if given.
    """
    def getLatestVideo(self):
        found = False
        
        part = 'snippet'
        maxResults = 1
        pageToken = None
        keyword = self.keyword
        for i in range(100):
            result = youtube.playlistItems().list(playlistId=self.getUploadsPlaylist(), part=part, maxResults=maxResults, pageToken=pageToken).execute()
            pageToken = result.get('nextPageToken')

            if keyword in result['items'][0]['snippet']['title']:
                return result['items']
        raise Exception("No video found")
        
    #Takes a list of 
    #Returns a list of datetime objects.
    @staticmethod
    def getTimestamp(video):
        #Apparently Python can't parse standard ISO-8601 properly.
        timeformat = "%Y-%m-%dT%H:%M:%SZ"
        return datetime.datetime.strptime(video['snippet']['publishedAt'], timeformat)
"""
    

    
class Hermit(YTChannel):
    
    def __init__(self, hermitID):
        super().__init__(hermitID.value['id'])
        self.keyword = hermitID.value['keyword']
