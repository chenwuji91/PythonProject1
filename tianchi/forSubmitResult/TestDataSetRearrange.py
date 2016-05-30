#-*- coding: UTF-8 -*-
'''
@author: chenwuji
提交结果处理的时候用  将生成的歌曲和歌手的混合数据进行转换  转换成最终的提交结果
读入文件夹的路径在为inpath定义  写入文件夹为outpath定义的文件名
'''

import numpy as np
import sys
import glob
import os
songToSinger = {}
songScore = {}
singerScore = {}
singerAllScoreByDate ={}
inpath = '/Users/chenwuji/Documents/skypool/测评相关/5-29/*'
outpath = '/Users/chenwuji/Documents/skypool/测评相关/PredictResult0529.txt'

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
    f = glob.glob(inpath)
    for eachFile in f:
        scoreList = []
        fileBaseName = os.path.basename(eachFile).split('.')[0]
        f2 = open(eachFile)
        for eachline in f2:
            scoreList.append(float(eachline))
        songScore.setdefault(fileBaseName,scoreList)

def calculateSingerScore():
    dateList = []
    for i in range(20150901, 20150931):
        dateList.append(i)
    for i in range(20151001, 20151031):
        dateList.append(i)
    for eachday in range(60):
        currentDaySingerScore = singerScore.copy()
        for eachsong in songScore:#对于每一个歌曲的评分
            currentSongOfTheDayScore = songScore.get(eachsong)[eachday]   #某一个歌曲当天的分数
            currentSinger = songToSinger.get(eachsong)  #找出这首歌对应的歌手
            currentScore = currentDaySingerScore.get(currentSinger)
            currentDaySingerScore.update({currentSinger:(currentScore + currentSongOfTheDayScore)})
        for singer in currentDaySingerScore:
            result = singer +','+ str(int(currentDaySingerScore.get(singer)))+','+str(dateList[eachday])

            writeToFile(outpath,result)

def writeToFile(fileName,data):
    f = file(fileName, "a+")
    f.writelines(data)
    f.writelines("\n")
    f.close()

if __name__ == '__main__':
    readTestList()
    readSingerSong()
    calculateSingerScore()