#thank you, kind stranger:
#https://stackoverflow.com/a/14190143/9342254
def convert_timedelta(duration):
    days, seconds = duration.days, duration.seconds
    hours = seconds // 3600
    return days, hours