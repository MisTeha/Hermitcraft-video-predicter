from googleapiclient.discovery import build
import datetime

APIKEY = "don't worry the last one's expired"
youtube = build('youtube', 'v3', developerKey=APIKEY)


class YTChannel:
    def __init__(self, channelId, keyword="", maxResults=20):
        assert isinstance(keyword, str)
        assert isinstance(maxResults, int) & 1 <= maxResults <= 50
        self.maxResults = maxResults
        self.channelId = channelId
        self.keyword = keyword
        self.videos = self.getChannelVideos()
        self.latestVideo = self.videos[0]

    # Returns the value of the uploads playlist id.
    def getUploadsPlaylist(self):
        return youtube.channels().list(id=self.channelId, part='contentDetails') \
            .execute()['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    # Returns a list of self's videos. Keyword being the filter, if given.
    def getChannelVideos(self):
        part = 'snippet'
        keyword = self.keyword
        pageToken = None
        videos = []

        n = 2
        # For loop in case the first result doesn't contain any videos with a matching keyword.
        # Raises an exception if none found after n loops.
        for i in range(n):
            result = youtube.playlistItems().list(
                playlistId=self.getUploadsPlaylist(),
                maxResults=self.maxResults,
                pageToken=pageToken,
                part=part
            ).execute()

            if keyword == "":
                return result['items']

            [videos.append(item) for item in result['items']
             if keyword in item['snippet']['title']]
            if len(videos) == 0:
                pageToken = result.get('nextPageToken')
                if pageToken is None:
                    break
        if len(videos) == 0:
            raise Exception("No videos found.")

        return videos[:6]
        # panin limiidiks 5 videot, kuna muidu võtaks programm liiga vana infot kasutusse.
        # Oleks tore, kui saaksin seda limiteerida juba maxResultsiga, aga enamus hermitid teevad ka teisi videoid,
        # seega, kui küsiksin youtubelt vaid 5 videot, oleksid keyworidga sobivad ilmselt ainult 2 või 3.
