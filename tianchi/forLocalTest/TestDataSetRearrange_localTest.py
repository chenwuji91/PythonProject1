#-*- coding: UTF-8 -*-
'''
@author: chenwuji
本地测评的时候使用   将生成的歌曲和歌手的混合数据进行转换  转换成最终的提交结果
读入文件夹的路径在为inpath定义  写入文件夹为outpath定义的文件名
'''
dataIn = '/Users/chenwuji/Documents/skypool/测评相关/3964ee41d4e2ade1957a9135afe1b8dc/*'
outroot = '/Users/chenwuji/Documents/skypool/测评相关/PredictResult_3964ee41d4e2ade1957a9135afe1b8dc.txt'

import numpy as np
import sys
import glob
import os
songToSinger = {}
songScore = {}
singerScore = {}
singerAllScoreByDate ={}


def readSingerSong():
    f = open('/Users/chenwuji/Documents/skypool/mars_tianchi_songs_withSinger.csv')
    for eachline in f:
        list1 = eachline.split(',')
        song = str(list1[0])
        singer = str(list1[1])
        songToSinger.setdefault(song,singer)
        singerScore.setdefault(singer,0.0)
    f.close()

def readTestList():
    f = glob.glob(dataIn)
    for eachFile in f:
        scoreList = []
        fileBaseName = os.path.basename(eachFile).split('.')[0]
        f2 = open(eachFile)
        for eachline in f2:
            scoreList.append(float(eachline))
        songScore.setdefault(fileBaseName,scoreList)

def calculateSingerScore():
    dateList = []
    for i in range(20150716, 20150732):
        dateList.append(i)
    for i in range(20150801, 20150831):
        dateList.append(i)
    for eachday in range(46):
        currentDaySingerScore = singerScore.copy()
        for eachsong in songScore:#对于每一个歌曲的评分
            currentSongOfTheDayScore = songScore.get(eachsong)[eachday]   #某一个歌曲当天的分数
            currentSinger = songToSinger.get(eachsong)  #找出这首歌对应的歌手
            currentScore = currentDaySingerScore.get(currentSinger)
            currentDaySingerScore.update({currentSinger:(currentScore + currentSongOfTheDayScore)})
        for singer in currentDaySingerScore:
            result = singer +','+ str(int(currentDaySingerScore.get(singer)))+','+str(dateList[eachday])

            writeToFile(outroot,result)

def writeToFile(fileName,data):
    f = file(fileName, "a+")
    f.writelines(data)
    f.writelines("\n")
    f.close()


if __name__ == '__main__':
    readTestList()
    readSingerSong()
    calculateSingerScore()