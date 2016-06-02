#-*- coding: UTF-8 -*-
'''
@author: chenwuji
'''
#本程序做数据归并
fileList = []
path1 = '/Users/chenwuji/Documents/苏州出租车/suzhou结果/路段分时段车速信息/'
path2 = '/Users/chenwuji/Documents/苏州出租车/ubuntu结果/suzhou/路段分时段车速信息/'
path3 = '/Users/chenwuji/Documents/苏州出租车/ubuntu结果/suzhou/路段分时段车速信息282930/'
path4 = '/Users/chenwuji/Documents/苏州出租车/windows结果/result/'
pathList = [path1,path2,path3,path4]
weekend = [3,4,10,11,18,17,25,24,31,1]

import glob
import os
def fileListAll():
    f = glob.glob(path1 + '*')
    for eachFile in f:
        fileBaseName = os.path.basename(eachFile)
        fileList.append(fileBaseName)


def writeToFile(fileName, data):
    f = file('/Users/chenwuji/Documents/苏州出租车/resultReduced2/' + fileName, "a+")
    f.writelines(data)
    f.close()

from datetime import datetime
def gather():
    for eachpath in pathList:
        for filename in fileList:
            try:
                f2 = open(eachpath + filename)
                for eachline in f2:
                    list1 = eachline.split(';')
                    if len(list1)>2:
                        datetime1 = list1[2].split(',')[1]
                        speed = int(list1[1])
                        ddd = datetime.strptime(datetime1, "%Y-%m-%d %H:%M:%S").day
                        if ddd not in weekend:
                            fileN = str(filename).split('_')[0]+'_'+str(filename).split('_')[1]
                            if speed > 5:
                                writeToFile(fileN,eachline)
                f2.close()
            except:
                pass

if __name__ == '__main__':
    fileListAll()
    gather()







        