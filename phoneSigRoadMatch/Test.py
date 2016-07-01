#-*- coding: UTF-8 -*-
'''
@author: chenwuji
'''

def increaseVote(index1):
    if (voteDict.__contains__(index1)):
        current  = voteDict.get(index1)
        voteDict.update({index1:current+1})
    else:
        voteDict.setdefault(index1,1)



voteDict = {}

def test(list1, k ):
    for i in range(0,len(list1[0:k])):
        # print '第一次'
        print list1[i]
    for j in range(len(list1[0:k+1]),len(list1)):
        # print '第二次'
        print list1[j]


if __name__ == '__main__':
    list1 = [10,20,30,40,50,60,70]
 #    print 'fuck'
 # #   for i in range(len(list1)-1,-1,-1):
 #  #      print list1[i]
 #    for i in range(7):
 #
 #        test(list1,i)
    for eachP1 in list1:
        for eachP2 in list1:
            print eachP1
            print eachP2
            print 'next'





    # voteDict.setdefault(1, 2)
    # voteDict.setdefault(5, 6)
    # increaseVote(3)
    # increaseVote(3)
    # increaseVote(3)
    # increaseVote(3)
    # increaseVote(1)
    # increaseVote(1)
    # increaseVote(1)
    # increaseVote(1)
    # increaseVote(1)
    # increaseVote(3)
    # increaseVote(3)
    # increaseVote(7)

    # for eachH in houxuanPointDict:
    #     print eachH
    #     pL = houxuanPointDict.get(eachH)
    #     # print pL
    #     for eachP in pL:
    #         print eachP.x
    #         print eachP.y
    #         print eachP.roadIntersection1
    #         print eachP.roadIntersection2

    # if type(houxuanPointDict.get(eachH)) == HouxuanPoint:
    #     print houxuanPointDict.get(eachH).x
    #     print houxuanPointDict.get(eachH).y
    #     print houxuanPointDict.get(eachH).roadIntersection1
    #     print houxuanPointDict.get(eachH).roadIntersection2

    # -*- coding:utf8-*-
    import matplotlib.pyplot as plt

    # G = graphGenerate()
    # print nearestPath(str(0),'764',G)
    # G.add_weighted_edges_from([(1, 2, 2.09), (2, 3, 9.19), (3, 7, 7.88)])
    # G.add_weighted_edges_from([(1, 4, 1.09), (4, 5, 0.19), (5, 7, 1.88)])
    # G.add_weighted_edges_from([(3, 1, 0.09), (1, 5, 1.19), (5, 7, 2.88)])
    # G.add_weighted_edges_from([(3, 5, 2.09), (3, 6, 9.19), (6, 7, 7.88)])
    # nx.draw(G)
    # print nx.shortest_path(G)
    # plt.savefig("youxiangtu.png")
    # plt.show()
    #
    # matrix1 = np.zeros((2,2))
    # for i in range(2):
    #     for j in range(2):
    #         matrix1[i][j] = (i+1)*(j+1)
    #
    # for i in range(2):
    #     for j in range(2):
    #         print matrix1[i][j]
    # # print max(matrix1)
    # list = [9,2,3,4,5,6]
    # index = list.index(min(list))
    # print index




    # print '两个候选集的相关信息为'
    # print eachPoint1.roadIntersection1 + ' '+ eachPoint1.roadIntersection2
    # print eachPoint2.roadIntersection1 + ' ' + eachPoint2.roadIntersection2
    # print "最短路径"
    # print sPath.path
    # print '实际点的距离'
    # print point12Dis
    # print '候选点的距离'
    # print sPath.length
    # print '距离相似度'
    # print sPath.dis_similarity
    # print '实际候选点经过的时间 '
    # print sPath.time
    # print '时间相似度'
    # print sPath.time_similarity