#-*- coding: UTF-8 -*-
'''
@author: chenwuji
读入原始数据 按照天来分类
'''
import tools
outputPath = '/Users/chenwuji/Documents/skypool/集群原始数据/原始数据按天对应歌手数据按照周/'
songToSinger = {}

def readSingerSong():
    f = open('/Users/chenwuji/Documents/skypool/p2_mars_tianchi_songs.csv')
    for eachline in f:
        list1 = eachline.split(',')
        song = str(list1[0])
        singer = str(list1[1])
        songToSinger.setdefault(song,singer)
    f.close()


from datetime import datetime
def dateTransfer(info4):
    month = datetime.strptime(info4, "%Y%m%d").month
    day = datetime.strptime(info4, "%Y%m%d").day
    week = datetime(2015, month, day).isocalendar()[1]
    return week



def process():
    f = open('/Users/chenwuji/Documents/skypool/p2_mars_tianchi_user_actions.csv')
    for eachline in f:
        eachline = eachline.split('\n')[0]
        user = eachline.split(',')[0]
        singer = songToSinger.get(eachline.split(',')[1])
        info2 = eachline.split(',')[2]
        info3 = eachline.split(',')[3]
        info4 = eachline.split(',')[4]
        week = dateTransfer(info4)


        eachline = user + ',' + singer + ',' + info2 + ',' + info3 + ',' + info4
        writeToFile(outputPath + str(week), eachline)
    f.close()

def writeToFile(fileName,data):
    f = file(fileName, "a+")
    f.writelines(data)
    f.writelines("\n")
    f.close()


if __name__ == '__main__':

    tools.makeDir(outputPath)
    readSingerSong()
    process()

