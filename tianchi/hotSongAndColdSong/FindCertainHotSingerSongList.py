#-*- coding: UTF-8 -*-
'''
@author: chenwuji
找出某个特定歌手的全部的热门歌曲
'''
outputPath = '/Users/chenwuji/Documents/skypool/HotSongAndColdSong/'
certainSinger = ['97de6333157f35467dff271d7afb0a23']
songToSinger = {}


def readSingerSong():
    f = open('/Users/chenwuji/Documents/skypool/mars_tianchi_songs.csv')
    for eachline in f:
        list1 = eachline.split(',')
        song = str(list1[0])
        singer = str(list1[1])
        songToSinger.setdefault(song,singer)

    f.close()


def readHotSong():
        f3 = open('/Users/chenwuji/Documents/skypool/hotSongList2.csv')
        for eachline in f3:
            eachline = eachline.split('\n')[0]
            # print eachline
            currentSinger = songToSinger.get(eachline)#查看这个热门歌曲属于哪个歌手
            # print currentSinger
            if currentSinger in certainSinger:
                print eachline
                writeToFile(outputPath+'hotSong_'+str(certainSinger[0]),eachline)

def writeToFile(fileName,data):

    f = file(fileName, "a+")
    f.writelines(data)
    f.writelines("\n")
    f.close()
if __name__ == '__main__':
    readSingerSong()
    readHotSong()