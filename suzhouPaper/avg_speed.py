#-*- coding: UTF-8 -*-
'''
@author: chenwuji
'''
#求平均速度

import tools
import os
sep = os.sep
rootpath = sep+ 'Users'+sep+'chenwuji'+sep+'Documents'+sep+'苏州出租车'+sep+''

import glob
import numpy as np

def getFileList(path):
    file_list = []
    fold_date_list = glob.glob(rootpath + path +'/*')
    for each_car_folder in fold_date_list:
        each_car_file = glob.glob(each_car_folder+'/*')
        for eachF in each_car_file:
            file_list.append(eachF)
    return file_list

def re_write_by_time_slot(each_car_path):
    f = open(each_car_path)
    print 'Done',
    print each_car_path
    for eachline in f:
        eachline = eachline.split('\n')[0]
        lineList = eachline.split(',')
        if len(lineList) > 6:
            car_speed = lineList[3]
            car_date = lineList[5]
            time_split = tools.timeTranslate(car_date)
            ifweekend = tools.getDay(car_date)
            tools.makeDir(rootpath + 'avg_speed'+'/time_split/')
            if car_speed!='0':
                tools.writeToFile(rootpath + 'avg_speed'+'/time_split/'+str(time_split)+'_'+str(ifweekend), car_speed+'\t')


def avg(each_split):
    f = open(each_split)
    list = []
    for eachline in f:
        list.append(float(eachline.split('\n')[0].split('\t')[0]))
    return np.mean(list)



if __name__ == '__main__':
    # file_list = getFileList('原始数据和中间结果/data/')
    # for eachF in file_list:
    #     re_write_by_time_slot(eachF)

    path = 'avg_speed'+'/time_split/'
    file_list = glob.glob(rootpath + path + '/*')
    print file_list
    for eachF in file_list:
        mean = avg(eachF)
        fn = os.path.basename(eachF)
        time = fn.split('_')[0]
        weekend = fn.split('_')[1]
        tools.writeToFile(rootpath + 'avg_speed/' + 'speedResult' + str(weekend), str(tools.timeRetranslate(int(time)))+',' + str(mean))



