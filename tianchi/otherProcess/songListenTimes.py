#-*- coding: UTF-8 -*-
'''
@author: chenwuji
统计歌曲或者歌手的 人均收听次数
'''

import numpy as np
import sys
import glob
import os
songListTimes = {}
songListPeople = {}
#收听次数文件:
listenTime = '/Users/chenwuji/Documents/skypool/HotSongAndColdSong/歌曲收听次数.csv'
#收听人数:
listenPeople = '/Users/chenwuji/Documents/skypool/HotSongAndColdSong/歌曲收听人数.csv'
#输出目录  该输出为文件夹输出
outroot = '/Users/chenwuji/Documents/skypool/HotSongAndColdSong/高频歌曲人均收听次数/'

def readSongListenTimes():
    f = open(listenTime)
    for eachline in f:
        eachline = eachline.split('\n')[0]
        list1 = eachline.split(',')
        key1 = str(list1[0])+','+str(list1[2])
        songListTimes.setdefault(key1,float(list1[1]))
    f.close()

def readSongListenPeople():
    f = open(listenPeople)
    for eachline in f:
        eachline = eachline.split('\n')[0]
        list1 = eachline.split(',')
        key1 = str(list1[0])+','+str(list1[2])
        songListPeople.setdefault(key1,float(list1[1]))
    f.close()

def writeToFile(fileName,data):
    # f = file(rootpath+"/路段分时段车速信息/"+fileName, "a+")
    f = file(fileName, "a+")
    f.writelines(data)
    f.writelines("\n")
    f.close()

def countTimesEveryday():
    for eachPerson in songListPeople:
        listenPersonCount = songListPeople.get(eachPerson)
        listenTimesCount = songListTimes.get(eachPerson)
        timesOfPersonOfThisSong = listenTimesCount/listenPersonCount
        # print timesOfPersonOfThisSong

        writeToFile(outroot +str(eachPerson).split(',')[0]+'.csv',str(timesOfPersonOfThisSong) +','+ str(eachPerson).split(',')[1])

if __name__ == '__main__':
    readSongListenPeople()
    readSongListenTimes()
    # print songListTimes
    # print songListPeople
    countTimesEveryday()
