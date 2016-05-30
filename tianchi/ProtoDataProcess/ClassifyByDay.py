#-*- coding: UTF-8 -*-
'''
@author: chenwuji
读入原始数据 按照天来分类
'''

outputPath = '/Users/chenwuji/Documents/skypool/集群原始数据/原始数据按天/'


def process():
    f = open('/Users/chenwuji/Documents/skypool/mars_tianchi_user_actions.csv')
    for eachline in f:
        eachline = eachline.split('\n')[0]
        writeToFile(outputPath+eachline.split(',')[4], eachline)
    f.close()

def writeToFile(fileName,data):
    f = file(fileName, "a+")
    f.writelines(data)
    f.writelines("\n")
    f.close()


if __name__ == '__main__':

    process()

