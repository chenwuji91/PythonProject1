#-*- coding: UTF-8 -*-
'''
@author: chenwuji
依据收听人数的数据  将收听人数下面出现的所有歌曲分类为冷门歌曲和热门歌曲 并将结果输出
'''


import glob
import os
hotSong = set()
coldSong = set()

def readSongList():
    f = glob.glob('/Users/chenwuji/Documents/skypool/集群原始数据/歌曲收听人数filled/*')
    for eachFile in f:
        fileBaseName = os.path.basename(eachFile).split('.')[0]
        f2 = open(eachFile)
        hot = True
        coldagain = True
        for eachline in f2:
            songListTime = int(eachline.split(',')[0])
            if songListTime == 0:
                if coldagain == False:
                    coldSong.add(fileBaseName)
                    hot = False
            if songListTime != 0:
                coldagain = False
        if hot == True:
            hotSong.add(fileBaseName)

def writeToFile(fileName,data):
    f = file(fileName, "a+")
    f.writelines(data)
    f.writelines("\n")
    f.close()


if __name__ == '__main__':
    readSongList()
    for eachH in hotSong:
        writeToFile('/Users/chenwuji/Documents/skypool/hotSongList2.csv',eachH)
    for eachC in coldSong:
        writeToFile('/Users/chenwuji/Documents/skypool/coldSongList2.csv',eachC)
