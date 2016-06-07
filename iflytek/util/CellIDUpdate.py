#-*- coding: UTF-8 -*-
'''
@author: chenwuji

'''
# 功能描述:本程序的主要是在基站信息更新之后执行本程序,将SVN上面经过更新的基站小区静态表转换成程序运行时候需要的参数.
#在基站信息更新之后 重新运行本程序



def readcellIdSheet():
    f = open('/Users/chenwuji/Documents/RoadMatch/Xiaoqu.csv')
    for eachline in f:
        list1 = eachline.split(',')
        try:
            eachline = eachline.split('\n')[0]
            nodeID = list1[5]
            longi = list1[3]
            lati = list1[4]
            range = int(list1[10])
            data1 = nodeID + '\t' +longi + '\t' +lati + '\t' +str(range) + '\t'
            writeToFile('/Users/chenwuji/Documents/RoadMatch/cellIdSheetOnlyXiaoQU.txt', data1)
        except:
            print eachline


    f.close()


def writeToFile(fileName,data):
    f = file(fileName, "a+")
    f.writelines(data)
    f.writelines("\n")
    f.close()

if __name__ == '__main__':
    readcellIdSheet()