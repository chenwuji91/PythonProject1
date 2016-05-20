#-*- coding: UTF-8 -*-
'''
@author: chenwuji
直接针对原始数据进行的一个处理,将原始用户行为的数据根据歌曲的热门冷门,对热门歌曲进行合并
'''

import numpy as np
import sys
import glob
import os
hotSong = []
coldSong = []
songToSinger = {}




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

def readSingerSong():
    f = open('/Users/chenwuji/Documents/skypool/mars_tianchi_songs_withSinger.csv')
    for eachline in f:
        list1 = eachline.split(',')
        song = str(list1[0])
        singer = str(list1[1])
        songToSinger.setdefault(song,singer)
    f.close()

def process():
    outpath = '/Users/chenwuji/Documents/skypool/user_actionHotCold.csv'
    f = open('/Users/chenwuji/Documents/skypool/mars_tianchi_user_actions.csv')
    for eachline in f:
        eachline = eachline.split('\n')[0]
        list1 = eachline.split(',')
        song = list1[1]
        if song in coldSong:
            theSinger = songToSinger.get(song)
            writeToFile(outpath, list1[0]+','+theSinger+','+list1[2]+','+list1[3]+','+list1[4])
        elif song in hotSong:
            writeToFile(outpath, eachline)
    f.close()

def writeToFile(fileName,data):
    f = file(fileName, "a+")
    f.writelines(data)
    f.writelines("\n")
    f.close()


if __name__ == '__main__':
    readcold()
    readhot()
    readSingerSong()
    process()

