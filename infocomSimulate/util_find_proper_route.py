
#-*- coding: UTF-8 -*-
'''
@author: chenwuji
定义规则,寻找合适的轨迹
'''
road_intersection = set()
camera_intersection = set()
import glob
import os
proper_path = []
def getFileList():
    f = glob.glob('car_route'+os.path.sep+'*')
    list = []
    for each in f:
        list.append(each)
    return list

def proper_road_intersection_set():
    f = open('data' + os.path.sep + 'datatemp')
    for eachline in f:
        road_intersection.add(eachline.split(',')[1].split('\r')[0].split('\n')[0])
        road_intersection.add(eachline.split(',')[0])
    f.close()

def read_carema():
    f = open('data' + os.path.sep + 'camera.txt.tempremove')
    for eachline in f:
        camera_intersection.add(eachline.split('\r')[0].split('\n')[0])
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
        if len(onepath) == 0 and rd_intersection in camera_intersection:
            onepath.append((rd_intersection,speed,time))
        elif len(onepath) > 0 and rd_intersection in road_intersection and speed > 5 and speed < 80:
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
        if intervals < 800:
            proper_path.append(each_path)

import uuid
def out_to_json():
    for each_path in proper_path:
        currentFile = str(uuid.uuid4())
        tools.writeToFile('route_2/'+currentFile,'[')
        for each_point in range(len(each_path) - 1):
            rd = each_path[each_point][0]
            speed = each_path[each_point][1]
            time = each_path[each_point][2]
            line = '{\"num\": \"'+ rd +'\", \"speed\": '+ str(speed) +', \"time\": \"'+ time+'\"},'
            tools.writeToFile('route_2/' + currentFile, line)
        rd = each_path[len(each_path) - 1][0]
        speed = each_path[len(each_path) - 1][1]
        time = each_path[len(each_path) - 1][2]
        line = '{\"num\": \"' + rd + '\", \"speed\": ' + str(speed) + ', \"time\": \"' + time + '\"}]'
        tools.writeToFile('route_2/' + currentFile, line)

if __name__ == '__main__':
    proper_road_intersection_set()
    read_carema()
    file_list = getFileList()
    for eachf in file_list:
        choose_proper_route(eachf)
    print proper_path
    out_to_json()