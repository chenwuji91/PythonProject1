#-*- coding: UTF-8 -*-
'''
@author: chenwuji
一个文件按照歌手或者歌曲(某一个标签)分成多个文件
'''

def writeToFile(fileName,data):

    f = file(fileName, "a+")
    f.writelines(data)
    f.close()

if __name__ == '__main__':
    f = open('/Users/chenwuji/Documents/skypool/mars_tianchi_artist_plays_predict.csv')
    for eachline in f:
        filename = eachline.split(',')[0]
        times = eachline.split(',')[1]
        day = eachline.split(',')[2]
        writeToFile('/Users/chenwuji/Documents/skypool/0523提交数据/'+filename+'.csv',times+ ','+day)


