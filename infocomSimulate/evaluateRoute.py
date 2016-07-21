#-*- coding: UTF-8 -*-
'''
@author: 张文
路段评分程序
'''
class comSubseq:
    def __init__(self):
        self.maxLen = 0  # common subsequence max length
        self.sequence = []  # record the sequence

#路口转换成路段
def transRoute(route) :
    result = []
    start = route[0][:]
    for i in range(1, len(route)) :
        temp = start.strip() + '-' + route[i].strip()
        result.append(temp)
        start = route[i][:]
    # print(result)
    return result

#求一个序列去掉自己的子序列
def removeCom(list, sublist) :
    result = []
    i = 0
    j = 0
    while i < len(list) and j < len(sublist) :
        if(list[i] == sublist[j]) :
            i += 1
            j += 1
        else :
            result.append(list[i])
            i += 1
    while i < len(list) :
        result.append(list[i])
        i = i + 1

    return result


#求两条路径的最大公共路段序列
def maxComSubseq(list1, list2) :
    fMatrix = []

    len1 = len(list1)
    len2 = len(list2)

    for i in range(len1 + 1) :
        listtemp = []
        for j in range(len2 + 1) :
            temp = comSubseq()
            listtemp.append(temp)
        fMatrix.append(listtemp)

    for i in range(len1) :
        for j in range(len2) :
            if(list1[i] == list2[j]) :
                fMatrix[i + 1][j + 1].maxLen = fMatrix[i][j].maxLen + 1
                fMatrix[i + 1][j + 1].sequence = fMatrix[i][j].sequence[:]
                fMatrix[i + 1][j + 1].sequence.append(list1[i])
            else :
                fMatrix[i + 1][j + 1].maxLen = max(fMatrix[i + 1][j].maxLen, fMatrix[i][j + 1].maxLen)
                if (fMatrix[i + 1][j].maxLen > fMatrix[i][j + 1].maxLen) :
                    fMatrix[i + 1][j + 1].sequence = fMatrix[i + 1][j].sequence[:]
                else :
                    fMatrix[i + 1][j + 1].sequence = fMatrix[i][j + 1].sequence[:]


    # print fMatrix[len1][len2].maxLen
    # print fMatrix[len1][len2].sequence
    return fMatrix[len1][len2].sequence


#路径测评
def evaluateFunc(realRoute, predictRoute) :
    realList = transRoute(realRoute)
    predictList = transRoute(predictRoute)

    commonList = maxComSubseq(realList, predictList)    # TT
    lessList = removeCom(realList, commonList)          # FT
    moreList = removeCom(predictList, commonList)        # TF
    return len(commonList),len(lessList),len(moreList)
    # print(lessList)
    # print(moreList)
    #
    # print(float(len(commonList)) / float(len(moreList)))
    if len(moreList) == 0:
        return float(len(commonList)) / (float(len(moreList))+ 0.0000001)
    return float(len(commonList)) / float(len(moreList))


#
# list1 = ['965', '1180', '979', '1210', '1119', '1012', '913', '1000', '1001', '983', '1058', '825', '800', '801', '802', '825', '803', '804', '802', '825', '1143', '947', '1136', '990']
# list2 = ['965', '1180', '52', '47', '979', '1210', '1119', '1012', '913', '983', '1058', '825','803', '804', '802', '825', '800', '801', '802', '825', '1143', '947', '1136', '947', '1136', '990']
# evaluateFunc(list1, list2)


