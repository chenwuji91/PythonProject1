# -*- coding: UTF-8 -*-
"""
@author: lbx
根据陈无忌需求
给定 时间 和 一车辆信息文件，文件格式如：
    [{"num": "865", "speed": 20, "time": "2016-10-1-12:00"},
    {"num": "1180", "speed": 20, "time": "2016-10-1-12:00"},
    ...
    {"num": "1180", "speed": 20, "time": "2016-10-1-12:00"}]
返回 （from， to，离from的距离d）三个参数
"""
import os
import re
# import roadBasic as rd
import tools

def int2str0(n):
    if n >= 10:
        return str(n)
    return '0' + str(n)

def str2int(s):
    """
    :param s='2012-03-02 10:22:23':
    :return: 当天从0时起经过的秒数
    """
    s1 = s.split(' ')[1].split(':')
    return int(s1[0]) * 3600 + int(s1[1]) * 60 + int(s1[2])
def int2str(n):
    hour = n / 3600
    minute = (n % 3600) / 60
    second = n % 60
    return int2str0(hour) + ':' + int2str0(minute) + ':' + int2str0(second)

def getinfo(time, filename, rd):
    with open('data_for_run' + os.path.sep+filename, 'r') as f:
        all_text_list = f.read().lstrip('[').strip('\r\n').strip('\n').rstrip(']')
        all_text_list = re.split(r'},\n{|},\r\n{', all_text_list)
        all_text_list[0] = all_text_list[0].lstrip('{')
        all_text_list[len(all_text_list)-1] = all_text_list[len(all_text_list)-1].rstrip('}')
        pre_time = all_text_list[0].split(', ')[2].split(': ')[1].strip('"')
        pre_from = all_text_list[0].split(', ')[0].split(': ')[1].strip('"')
        for i, each in enumerate(all_text_list):
            each = each.split(', ')
            now_time = each[2].split(': ')[1].strip('"')
            to = each[0].split(': ')[1].strip('"')
            if pre_time > time:  # 查询时间小于第一条记录时间，则失败
                return None
            if now_time >= time > pre_time:  # 定位到now_time
                now_t = str2int(now_time)
                pre_t = str2int(pre_time)
                dt = float(now_t - pre_t)  # 整个该路段的时间间隔
                percent = (str2int(time) - pre_t) / dt  # 根据时间所占的比例，计算出距离
                # print pre_from
                # print to
                d = rd.getRoadLen(pre_from, to) * percent
                return pre_from, to, d
            pre_time = now_time
            pre_from = to
        return None  # 没有查询到合适的记录，查询失败

if "__main__" == __name__:
    while True:  # TEST
        s = raw_input("please input file name and check time\n")
        s = s.split(',')
        print getinfo(s[1], s[0])
# 20120321_3565.txt_868f0f00-433c-11e6-90db-3497f625b127,2012-03-22 07:05:10
