
#-*- coding: UTF-8 -*-
'''
@author: chenwuji
定义规则,寻找合适的轨迹
'''
road_intersection = set()
import glob
import os
proper_path = []
def getFileList():
    f = glob.glob('car_route/*')
    list = []
    for each in f:
        list.append(each)
    return list

def proper_road_intersection_set():
    f = open('data' + os.path.sep + 'datatemp')
    for eachline in f:
        road_intersection.add(eachline.split(',')[1])
        road_intersection.add(eachline.split(',')[0])
    f.close()

import tools
def choose_proper_route(filename):
    path1 = []
    f = open(filename)
    onepath = []
    for eachline in f:
        rd_intersection = eachline.split(',')[0].split('\"num\": \"')[1].split('\"')[0]
        speed = int(eachline.split(',')[1].split('\"speed\": ')[1])
        time = eachline.split(',')[2].split('\"time\": \"')[1].split('\"')[0]

        if rd_intersection in road_intersection and speed > 20 and speed < 80:
            onepath.append((rd_intersection,speed,time))
        else:
            if len(onepath) > 20:
                path1.append(onepath)
            onepath = []
    f.close()

    for each_path in path1:
        time1 = each_path[0][2]
        time2 = each_path[len(each_path)-1][2]
        intervals = tools.intervalofSeconds(time1, time2)
        if intervals < 600:
            proper_path.append(each_path)

import uuid
def out_to_json():
    for each_path in proper_path:
        currentFile = str(uuid.uuid4())
        tools.writeToFile('route_2/'+currentFile,'[')
        for each_point in each_path:
            rd = each_point[0]
            speed = each_point[1]
            time = each_point[2]
            line = '{\"num\": \"'+ rd +'\", \"speed\": '+ str(speed) +', \"time\": \"'+ time+'\"},'
            tools.writeToFile('route_2/' + currentFile, line)
        tools.writeToFile('route_2/' + currentFile, ']')

if __name__ == '__main__':
    proper_road_intersection_set()
    file_list = getFileList()
    for eachf in file_list:
        choose_proper_route(eachf)
    print proper_path
    out_to_json()