#-*- coding: UTF-8 -*-
'''
@author: chenwuji
'''


def writeToMapForm(lukouDict,outPath,dataList):
    import tools
    dataList = tools.process(dataList)
    if len(dataList)<1:
        return
    s = '{"geo":['
    for eachP in dataList:
        lati = lukouDict.get(eachP).x
        longi = lukouDict.get(eachP).y
        s = s + '[' + str(lati) + ',' + str(longi) + '],'
    s = s[0:len(s)-1] + '],"count":"1"},'
    tools.writeToFile(outPath, s)
    print s
