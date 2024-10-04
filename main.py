from utils.hermitids import HermitIDs
from utils.hermit import Hermit
import sys

def main(testresponse=None):
    if testresponse is None:
        while True:
            response = input("Kirjuta hermiti nimi, et teada saada, millal ta uus video ilmuma peaks. Kirjuta 'list', et näha kõiki hermiteid. \n")
            
            if response.lower() == "list":
                print(getAllHermitsStr() + "\n")
                continue
            elif response == "<<all":
                for hermitid in HermitIDs:
                    main(hermitid.value['displayName'])
                sys.exit()
            
            try:
                hermitID = getHermit(response)
            except Exception as e:
                print(e)
                continue
            break
    else:
        response = testresponse
        hermitID = getHermit(response)
    
    hermit = Hermit(hermitID)
    
    if hermit.timeUntilNextVideo.days < 0:
        timestr = convertTimedelta(hermit.timeUntilNextVideo * -1, False)
        print(f"{hermit.displayname} uus HermitCrafti video on hiljaks jäänud. Ootasime videot {timestr} tagasi.")
        return

    timestr = convertTimedelta(hermit.timeUntilNextVideo)
    print(f"{hermit.displayname} uus Hermitcrafti video peaks tulema umbes {timestr} pärast.")

    if (hermit.timeSinceLastVideo.total_seconds() / 3600) < (hermit.averagePeriod.total_seconds() / 3600 / 4):
        timestr = convertTimedelta(hermit.timeSinceLastVideo, False)
        videoid = hermit.latestVideo['snippet']['resourceId']['videoId']
        print(f"Kas teadsid, et {hermit.displayname} laadis oma viimatise Hermitcrafti video {timestr} tagasi. \n" +
            f"Link sellele videole: https://www.youtube.com/watch?v={videoid}")


def getHermit(name):
    for hermit in HermitIDs:
        if hermit.value['displayName'].lower() == name.lower(): return hermit
    raise Exception(f"Ei leidnud hermitit nimega {name}.")
    
def getAllHermitsStr():
    allhermits = ""
    for hermit in HermitIDs:
        allhermits = f"{allhermits}{hermit.value['displayName']}, "
    return allhermits[:-2] + "."
        
#thank you, kind stranger
#https://stackoverflow.com/a/14190143/9342254
def convertTimedelta(duration, present=True):
    days = int(duration.total_seconds() // 86400)
    hours = round(duration.total_seconds() % 86400 / 3600)

    if present:
        if days <= 0:
            return f"{hours} tunni"
        else:
            return f"{days} päeva ja {hours} tunni"
    else:
        if days <= 0:
            return f"{hours} tund{'i' if hours != 1 else ''}"
        else:
            return f"{days} päev{'a' if days != 1 else ''} ja {hours} tund{'i' if hours != 1 else ''}"

if __name__ == "__main__":
    main()