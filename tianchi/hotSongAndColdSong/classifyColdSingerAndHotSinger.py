#-*- coding: UTF-8 -*-
'''
@author: chenwuji
输出冷门歌手和热门歌手的收听次数的详细信息   冷门歌手输出歌手的全部收听次数  热门歌手输出单个歌曲的收听次数
'''

import numpy as np
import sys
import glob
import os
import tools
hotSong = []
coldSong = []
songListTimes = []
songToSinger = {}
singerScoreWithDate = {}



def readcold():
    f = open('/Users/chenwuji/Documents/skypool/coldSongList2.csv')
    for eachline in f:
        coldSong.append(str(eachline.split('\n')[0]))
    f.close()

def readhot():
    f = open('/Users/chenwuji/Documents/skypool/hotSongList2.csv')
    for eachline in f:
        hotSong.append(str(eachline.split('\n')[0]))
    f.close()

def readSong():
    f = open('/Users/chenwuji/Documents/skypool/集群原始数据/歌曲收听次数.csv')
    for eachline in f:
        eachline = eachline.split('\n')[0]
        list1 = eachline.split(',')
        key1 = str(list1[0])+','+str(list1[2])
        songListTimes.append((key1,int(list1[1])))
    f.close()

def readSingerSong():
    f = open('/Users/chenwuji/Documents/skypool/p2_mars_tianchi_songsWithSinger.csv')
    for eachline in f:
        list1 = eachline.split(',')
        song = str(list1[0])
        singer = str(list1[1])
        songToSinger.setdefault(song,singer)
    f.close()


def calculateSingerScore():
    for eachSongWithDate in songListTimes:
        songId = str(eachSongWithDate[0]).split(',')[0]
        date = str(eachSongWithDate[0]).split(',')[1]
        if songId in hotSong:
            tools.makeDir('/Users/chenwuji/Documents/skypool/HotSongAndColdSong/')
            tools.makeDir('/Users/chenwuji/Documents/skypool/HotSongAndColdSong/song/')
            writeToFile('/Users/chenwuji/Documents/skypool/HotSongAndColdSong/song/'+songId+'.csv', str(eachSongWithDate[1]) + ',' + date)
            # writeToFile('/Users/chenwuji/Documents/cwj.tianchi.forLocalTest/HotSongAndColdSong/歌曲收听人数.csv',
            #         songId+','+str(eachSongWithDate[1]) + ',' + date)

        # elif songId in coldSong:
        else:
            currentSinger = songToSinger.get(songId)  # 找出这首歌对应的歌手
            currentSingerWithDate = currentSinger + ',' + date
            if (singerScoreWithDate.__contains__(currentSingerWithDate)):
                currentScore = singerScoreWithDate.get(currentSingerWithDate)
                newScore = currentScore + int(eachSongWithDate[1])
                singerScoreWithDate.update({currentSingerWithDate: newScore})
            else:
                singerScoreWithDate.setdefault(currentSingerWithDate,int(eachSongWithDate[1]))
        # else:
        #     print "Cuo!"
        #     sys.exit(-1)

    for eachSinger in singerScoreWithDate:
        singer = str(eachSinger).split(',')[0]
        date2 = str(eachSinger).split(',')[1]
        tools.makeDir('/Users/chenwuji/Documents/skypool/HotSongAndColdSong/')
        tools.makeDir('/Users/chenwuji/Documents/skypool/HotSongAndColdSong/singer/')
        writeToFile('/Users/chenwuji/Documents/skypool/HotSongAndColdSong/singer/' + singer +'.csv', str(singerScoreWithDate.get(eachSinger)) + ',' + date2)
#上面的是批量输出  下面的是输出到单个文件
        # writeToFile('/Users/chenwuji/Documents/cwj.tianchi.forLocalTest/HotSongAndColdSong/歌手收听人数.csv', singer+','+str(singerScoreWithDate.get(eachSinger)) + ',' + date2)

def writeToFile(fileName,data):
    f = file(fileName, "a+")
    f.writelines(data)
    f.writelines("\n")
    f.close()


if __name__ == '__main__':
    readcold()
    readhot()
    readSong()
    readSingerSong()
    calculateSingerScore()
