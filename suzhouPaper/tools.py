
#-*- coding: UTF-8 -*-
'''
@author: chenwuji
'''


from datetime import datetime
def timeTranslate(date):
    h = datetime.strptime(date, "%Y-%m-%d %H:%M:%S").hour
    m = datetime.strptime(date, "%Y-%m-%d %H:%M:%S").minute
    timeSplit = int((h * 60 + m)/30) + 1
    return timeSplit

def timeRetranslate(time):
    hour = int(time/2)
    minute = int(time%2) * 30
    return str(hour) + ':' + str(minute)


weekend = [3,4,10,11,18,17,25,24,31,1]
def getDay(date):
    d = datetime.strptime(date, "%Y-%m-%d %H:%M:%S").day
    if d in weekend:
        return 1
    else:
        return 0


def writeToFile(fileName,data):
    f = file(fileName, "a+")
    f.writelines(data)
    f.writelines("\n")
    f.close()


