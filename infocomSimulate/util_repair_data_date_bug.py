
#-*- coding: UTF-8 -*-
'''
@author: chenwuji
修改日期错误的bug   重新修复日期
'''

import glob
import os
import roadBasic as rd
rd.initRoadData()
def getFileList():
    f = glob.glob('data_need_to_repair'+os.path.sep+'*')
    list = []
    for each in f:
        list.append(each)
    return list


import tools
def choose_proper_route(filename):
    f = open(filename)
    onepath = []
    for eachline in f:
        if len(eachline.split(',')) < 2:
            continue
        # print eachline.split(',')[0]
        # print eachline.split(',')[0].split('\"num\": \"')[1]
        # print eachline.split(',')[0].split('\"num\": \"')[1].split('\"')[0]

        rd_intersection = eachline.split(',')[0].split('\"num\": \"')[1].split('\"')[0]
        speed = int(eachline.split(',')[1].split('\"speed\": ')[1])
        time = eachline.split(',')[2].split('\"time\": \"')[1].split('\"')[0]
        if len(onepath) == 0:
            onepath.append((rd_intersection,speed,time))
        elif len(onepath) > 0:
            onepath.append((rd_intersection,speed,time))
    f.close()
    path1_1 = []
    begin_time = onepath[0][2]
    path1_1.append(onepath[0])
    for i in range(1,len(onepath)):
        # print onepath[i-1][0]
        # print onepath[i][0]
        dis = rd.getRoadLen(onepath[i-1][0],onepath[i][0])
        time1 = int(dis/(onepath[i][1]/3.6))
        timeNew = tools.increase_several_seconds(path1_1[i-1][2], time1)
        path1_1.append((onepath[i][0],onepath[i][1],timeNew))
    return path1_1


def out_to_json(currentFile,each_path):

        tools.writeToFile('data_for_run/'+currentFile,'[')
        for each_point in range(len(each_path) - 1):
            rd = each_path[each_point][0]
            speed = each_path[each_point][1]
            time = each_path[each_point][2]
            line = '{\"num\": \"'+ rd +'\", \"speed\": '+ str(speed) +', \"time\": \"'+ time+'\"},'
            tools.writeToFile('data_for_run/' + currentFile, line)
        rd = each_path[len(each_path) - 1][0]
        speed = each_path[len(each_path) - 1][1]
        time = each_path[len(each_path) - 1][2]
        line = '{\"num\": \"' + rd + '\", \"speed\": ' + str(speed) + ', \"time\": \"' + time + '\"}]'
        tools.writeToFile('data_for_run/' + currentFile, line)

if __name__ == '__main__':
    # proper_road_intersection_set()
    # read_carema()
    file_list = getFileList()
    for eachf in file_list:
        print eachf
        path1_1 = choose_proper_route(eachf)
        out_to_json(os.path.basename(eachf), path1_1)