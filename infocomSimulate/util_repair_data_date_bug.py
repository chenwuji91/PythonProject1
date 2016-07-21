
#-*- coding: UTF-8 -*-
'''
@author: chenwuji
修改日期错误的bug   重新修复日期
'''

import glob
import os
import roadBasic as rd
import random

rd.initRoadData()

def getFileList(read_path):
    f = glob.glob(read_path+os.path.sep+'*')
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

def read_file_and_check(file_path):
    f = open(file_path)
    all_data = []
    for eachline in f:
        eachline = eachline.split('\r')[0].split('\n')[0].split(';')[0]
        all_data.append(eachline)
    if len(all_data) < 4:
        print 'check file:',
        print os.path.basename(file_path)
        exit(-1)
    realpath = all_data[0]
    dijkstra_path = all_data[1]
    least_angle = all_data[2]
    path_type = int(all_data[3])
    tools.writeToFile('other_method_1_3'+ os.path.sep + str(os.path.basename(file_path)) + '-2'+ str(path_type)+'.dijkstra',
                      str(os.path.basename(file_path)).split('.txt')[0] + '-2' +',real path:[' + realpath + '],predict path:[' +
                      dijkstra_path + '],final score: 9999')
    tools.writeToFile('other_method_1_3' + os.path.sep + str(os.path.basename(file_path)) + '-2'+ str(path_type) + '.minAngle',
                      str(os.path.basename(file_path)).split('.txt')[
                          0]  + '-2'+ ',real path:[' + realpath + '],predict path:[' +
                      least_angle + '],final score: 9999')

    realpath_list = realpath.split(',')
    realpath_result = []

    begin_day =  int(random.uniform(11,30))
    begin_time = int(random.uniform(70,200))
    current_time = '2012-03-'+ str(begin_day) + ' ' + str(tools.timeRetranslate(begin_time)) + ':' + str(int(random.uniform(11,60)))
    begin_speed = int(random.uniform(45,59))
    realpath_result.append((realpath_list[0],begin_speed, current_time))
    for i in range(1,len(realpath_list)):
        current_rd_intersection = eachline
        speed = rd.getRoadSpeedAvg(realpath_list[i-1],realpath_list[i],str(tools.timeTranslate(current_time)),tools.getDay(current_time))
        if speed == None:
            speed = 53
        speed = int(speed)
        road_length = rd.getRoadLen(realpath_list[i-1], realpath_list[i])
        time_increase = int(road_length/(speed/3.6))
        current_time = tools.increase_several_seconds(current_time, time_increase)
        realpath_result.append((realpath_list[i], speed, current_time))

    return realpath_result


def removeDir(path):
    import os
    import shutil
    rootdir = path
    filelist = os.listdir(rootdir)
    for f in filelist:
        filepath = os.path.join(rootdir, f)
        if os.path.isfile(filepath):
            os.remove(filepath)
            print filepath + " removed!"
        elif os.path.isdir(filepath):
            shutil.rmtree(filepath, True)
            print "dir " + filepath + " removed!"

if __name__ == '__main__':



    removeDir('other_method_1_3')
    removeDir('data_for_run')
    rd.initSpeedData()
    file_list = getFileList('create_path')
    for eachf in file_list:
        try:
            # print eachf
            path1_1 = read_file_and_check(eachf)
            # path1_1 = choose_proper_route(eachf)
            out_to_json(os.path.basename(eachf) + '-2', path1_1)
        except:
            print 'fail path',
            print eachf