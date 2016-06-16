#-*- coding: UTF-8 -*-
'''
@author: chenwuji
'''

dataIn = '/Users/chenwuji/Documents/skypool/新方法/PublishDate/*'

import numpy
import glob
def getMean():
    f = glob.glob(dataIn)
    for eachFile in f:
        f1 = open(eachFile)
        num = []
        for eachLine in f1:
            eachLine = eachLine.split('\n')[0]
            num.append(float(eachLine.split(',')[1]))
        print eachFile,
        print numpy.mean(num)




if __name__ == '__main__':
    getMean()
