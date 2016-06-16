#-*- coding: UTF-8 -*-
'''
@author: chenwuji
'''

import tools

dataIn = '/Users/chenwuji/Documents/skypool/集群原始数据/原始数据按天/'
dataOut = '/Users/chenwuji/Documents/skypool/新方法/'
userListPath = 'UserList/'
songListenTime = 'SongListenTime/'
songCount = 'SongCount/'
singerCount = 'SingerCount/'
tools.makeDir(dataOut)
tools.makeDir(dataOut + userListPath)
# tools.removeDir(dataOut + userListPath)
tools.makeDir(dataOut + songListenTime)
tools.makeDir(dataOut + songCount)
tools.makeDir(dataOut + singerCount)
# tools.removeDir(dataOut + songListenTime)
date1 = ['20150501','20150430','20150429','20150428','20150427','20150426','20150425']
date2 = ['20150531','20150530','20150529','20150528','20150527','20150526','20150525']
date3 = ['20150324','20150323','20150329','20150328','20150327','20150326','20150325']
date4 = ['20150314','20150313','20150312','20150311','20150310','20150309','20150308']
date5 = ['20150506','20150505','20150504','20150503','20150502','20150501','20150430']
point = [('40d549e1310ae3ac82c318db775a7cce', '20150502', date1),
         ('40d549e1310ae3ac82c318db775a7cce', '20150601', date2),
         ('bcff0374e8fd6ece0a5d3658e41b9634', '20150330', date3),
         ('8a27d9a6c59628c991c154e8d93f412e', '20150315', date4),
         ('0827a03c7ff7175d7d284b4aa1966d5d' ,'20150507', date5)]
songToSinger = {}
songDateDict = {}


def process():
    for eachP in point:
        userList = getUserList(eachP[1], eachP[0])
        userSet =  set()
        for eachL in userList:
            userSet.add(eachL)
        for eachS in userSet:
            writeToFile(dataOut + userListPath + eachP[0] + '-' +eachP[1], eachS)
        # 开始看每个用户在这里面



        songList = getSong(eachP[2], userList)  #得到跟这些用户和这些日期相关的听歌事务数据

        # 获得某一部分用户群  的所有歌曲的收听次数
        dictUser = {}
        for eachS in songList:
            if dictUser.__contains__(eachS[0]):
                currentCount = dictUser.get(eachS[0])
                listenCount = currentCount + 1
                dictUser.update({eachS[0]:listenCount})
            else:
                dictUser.setdefault(eachS[0],1)
        print dictUser
        for eachUser in dictUser:
            writeToFile(dataOut + songListenTime + eachP[0] + '-' +eachP[1], eachUser + ',' + str(dictUser.get(eachUser)))

        #获得歌曲的收听广度
        dictUser = {}
        songSet = set()
        for song in songList:
            songSet.add((song[0],song[1]))
        for eachS in songSet:
            if dictUser.__contains__(eachS[0]):
                currentCount = dictUser.get(eachS[0])
                listenCount = currentCount + 1
                dictUser.update({eachS[0]: listenCount})
            else:
                dictUser.setdefault(eachS[0], 1)
        for eachUser in dictUser:
            writeToFile(dataOut + songCount + eachP[0] + '-' + eachP[1],
                        eachUser + ',' + str(dictUser.get(eachUser)))

        #获得歌手的收听广度
        dictUser = {}
        songSet = set()
        for song in songList:
            songSet.add((song[0],songToSinger.get(song[1])))
        for eachS in songSet:
            if dictUser.__contains__(eachS[0]):
                currentCount = dictUser.get(eachS[0])
                listenCount = currentCount + 1
                dictUser.update({eachS[0]: listenCount})
            else:
                dictUser.setdefault(eachS[0], 1)
        for eachUser in dictUser:
            writeToFile(dataOut + singerCount + eachP[0] + '-' + eachP[1],
                        eachUser + ',' + str(dictUser.get(eachUser)))


        #计算所听歌曲发型日期距离当前收听时间的天数



def readSingerSong():
    f = open('/Users/chenwuji/Documents/skypool/p2_mars_tianchi_songsWithSinger.csv')
    for eachline in f:
        list1 = eachline.split(',')
        song = str(list1[0])
        singer = str(list1[1])
        publish_date = str(list1[2])
        songToSinger.setdefault(song, singer)
        songDateDict.setdefault(song, publish_date)
    f.close()


def getSong(datelist, userList):
    dict = []
    for filename in datelist:
        f = open(dataIn + filename)
        for eachline in f:
            eachline = eachline.split('\n')[0]
            list1 = eachline.split(',')
            listUser = list1[0]
            song = list1[1]
            actionType = int(list1[3])
            date = list1[4]
            if actionType == 1:
                if listUser in userList:
                    dict.append((listUser, song, date))
    return dict

def getUserList(filename,songID):
    dict = []
    f = open(dataIn + filename)
    for eachline in f:
        eachline = eachline.split('\n')[0]
        list1 = eachline.split(',')
        listUser = list1[0]
        song = list1[1]
        actionType = int(list1[3])
        date = list1[4]
        if actionType == 1:
            if song == songID:
                dict.append(listUser)
    return dict



def writeToFile(fileName,data):
    f = file(fileName, "a+")
    f.writelines(data)
    f.writelines("\n")
    f.close()

if __name__ == '__main__':
    readSingerSong()
    process()