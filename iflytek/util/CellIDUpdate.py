#-*- coding: UTF-8 -*-
'''
@author: chenwuji
'''



def readcellIdSheet():
    f = open('/Users/chenwuji/Documents/RoadMatch/cellNew.csv')
    for eachline in f:
        list1 = eachline.split(',')
        try:
            eachline = eachline.split('\n')[0]
            nodeID = list1[5]
            longi = list1[3]
            lati = list1[4]
            range = int(list1[10])
            data1 = nodeID + '\t' +longi + '\t' +lati + '\t' +str(range) + '\t'
            writeToFile('/Users/chenwuji/Documents/RoadMatch/cellIdSheet.txt', data1)
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