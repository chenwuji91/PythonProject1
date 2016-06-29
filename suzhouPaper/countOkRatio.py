#-*- coding: UTF-8 -*-
'''
@author: chenwuji
'''

tobeChecked = '按照瞬时速度检验标准正态的时间结果'

inPath = '/Users/chenwuji/Documents/苏州出租车/'+tobeChecked+'/按照日期的检验平均速度/'
outPath = '/Users/chenwuji/Documents/苏州出租车/'+tobeChecked+'/'
import glob
import tools
import os
import numpy
def fileListAll():
    f = glob.glob(inPath + '*')

    for eachFile in f:
        countOneFile = 0.0
        countOkRecord = 0.0
        speedListOfThisTime = []
        f1 = open(eachFile)
        for eachLine in f1:
            countOneFile = countOneFile + 1.0
            ratio = float(eachLine.split(',')[0])
            currentSpeed = float(eachLine.split(',')[3])
            if ratio > 0.05:
                countOkRecord = countOkRecord + 1.0
                speedListOfThisTime.append(currentSpeed)
        f1.close()
        timeName = os.path.basename(eachFile).split('.')[0]
        weekend = timeName.split('_')[1]
        timeRecord = int(timeName.split('_')[0])
        timeRecord = tools.timeRetranslate(timeRecord)
        tools.writeToFile(outPath + weekend +'OKRatio.csv', timeRecord + ',' + str(countOkRecord/countOneFile)
                           + ',' +str(numpy.mean(speedListOfThisTime)))

if __name__ == '__main__':
    fileListAll()



