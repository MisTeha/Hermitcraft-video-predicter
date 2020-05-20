from ApiUtils import YTChannel
from hermits import HermitIDs

mumbo = YTChannel(HermitIDs.LINUSTECH.value['id'])

print(mumbo.averagePeriod / 1000 / 60 / 60)
print(mumbo.getTimeUntilNextVideo() / 1000 / 60 / 60)

