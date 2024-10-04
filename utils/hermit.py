from utils.apiutils import YTChannel
import datetime

class Hermit(YTChannel):
    def __init__(self, hermitID):
        super().__init__(hermitID.value['id'], hermitID.value['keyword'])
        self.displayname = hermitID.value['displayName']
    
    #Returns self's average time between uploads
    @property
    def averagePeriod(self):
        timestamps = [self.getDatetime(video) for video in self.videos]
        return self.getAveragePeriod(timestamps)

    #Returns a timedelta of time since the last video.
    @property
    def timeSinceLastVideo(self):
        sinceLastVideo = datetime.datetime.utcnow().timestamp() - self.getDatetime(self.latestVideo).timestamp()
        return datetime.timedelta(seconds=sinceLastVideo)

    #Returns a timedelta of estimated time until the next video
    @property
    def timeUntilNextVideo(self):
        sinceLastVideo = self.timeSinceLastVideo.total_seconds()
        period = self.averagePeriod.total_seconds()
        time = period - sinceLastVideo
        return datetime.timedelta(seconds=time)

    #Returns a datetime from playListItem
    @staticmethod
    def getDatetime(video):
        #apparently python's standard library can't properly parse standard ISO..
        timeformat = "%Y-%m-%dT%H:%M:%SZ"
        return datetime.datetime.strptime(video['snippet']['publishedAt'], timeformat)
    
    #Returns a timedelta of avarage difference between timestamps.
    @staticmethod
    def getAveragePeriod(timestamps):
        assert isinstance(timestamps, list), "Timestamps must be a list"
        time = 0
        for i in range(len(timestamps) - 1):
            time += timestamps[i].timestamp() - timestamps[i + 1].timestamp()
        averageTime = time / (len(timestamps)) -1
        return datetime.timedelta(seconds=averageTime)