#-*- coding: UTF-8 -*-
'''
@author: chenwuji
读取目录  并对目录内的文件进行按照日期的排序 其中数据只有两列  第一列为数值  第二列为日期
'''
import glob
import os

from cwj.tianchi.otherProcess import songListenTimes as lstimes


def readFile():

    f2 = glob.glob('/Users/chenwuji/Documents/skypool/HotSongAndColdSong/Singer/*')
    for file2 in f2:
        dict = {}
        filename2 = os.path.basename(file2)
        print '当前正在处理文件:' +  filename2
        f3 = open('/Users/chenwuji/Documents/skypool/HotSongAndColdSong/Singer/'+filename2)
        for eachline in f3:
            list1 = eachline.split('\n')[0].split(',')
            key1 = list1[1]
            value1 = int(list1[0])
            dict.setdefault(key1,value1)
        dict1 = sorted(dict.iteritems(), key=lambda d: d[0])
        for eachdict in dict1:
             lstimes.writeToFile('/Users/chenwuji/Documents/skypool/HotSongAndColdSong/SingerSorted/'+filename2,str(eachdict[1])+","+ str(eachdict[0]))
        f3.close()
if __name__ == '__main__':
    readFile()