#-*- coding: UTF-8 -*-
'''
@author: chenwuji
路段评分程序
'''
import os
import evaluateRoute as er
import tools

sep = os.path.sep
import glob
def getFileList(filepath):
    flist =  glob.glob(filepath + sep + '*')
    return flist


def read_other_method(other_method_root):
    flist = glob.glob('data/Result_sparse/'+ other_method_root +'/*')
    one_result_set = {}
    for each_file in flist:
        print each_file
        if other_method_root == 'method2':
            read_other_result2(each_file, one_result_set)
        else:
            read_other_result(each_file, one_result_set)
    return one_result_set

def read_other_result(filename_of_one, resultSet):
    f = open(filename_of_one)
    for eachline in f:
        if len(eachline.split(',')) < 2 :
            continue
        eachline = eachline.split('\n')[0].split('\r')[0]
        fileName = eachline.split(',real path:')[0]
        realPatht = eachline.split(',real path:')[1].split(',predict path:')[0]
        predictPatht = eachline.split(',real path:')[1].split(',predict path:')[1].split(',final score:')[0]
        finalScore = eachline.split(',real path:')[1].split(',predict path:')[1].split(',final score:')[1]

        realPatht = realPatht.split(',')
        realPath = []
        for eachl in realPatht:
            eachl = eachl.split('\'')[0]
            realPath.append(eachl)
        predictPatht = predictPatht.split(',')
        predictPath = []
        for eachl in predictPatht:
            eachl = eachl.split('\'')[0]
            predictPath.append(eachl)
        if len(fileName.split('.txt')) > 1:
            fileName = fileName.split('.txt')[0] + fileName.split('.txt')[1]
        resultSet.setdefault(fileName,(realPath, predictPath, finalScore))

    f.close()

def read_other_result2(filename_of_one, resultSet):
    f = open(filename_of_one)
    for eachline in f:
        if len(eachline.split(',')) < 2 :
            continue
        eachline = eachline.split('\n')[0].split('\r')[0]
        fileName = eachline.split(',real path:')[0]
        realPatht = eachline.split(',real path:')[1].split(',predict path:')[0]
        predictPatht = eachline.split(',real path:')[1].split(',predict path:')[1].split(',final score:')[0]
        finalScore = eachline.split(',real path:')[1].split(',predict path:')[1].split(',final score:')[1]

        realPatht = realPatht.split(',')
        realPath = []
        for eachl in realPatht:
            eachl = eachl.split('\'')[1]
            realPath.append(eachl)
        predictPatht = predictPatht.split(',')
        predictPath = []
        for eachl in predictPatht:
            eachl = eachl.split('\'')[1]
            predictPath.append(eachl)
        if len(fileName.split('.txt')) > 1:
            fileName = fileName.split('.txt')[0] + fileName.split('.txt')[1]
        resultSet.setdefault(fileName,(realPath, predictPath, finalScore))
    f.close()


def read_our_method(other_method_root):
    flist1 = glob.glob('data/Result_sparse/'+ other_method_root +'/*')
    flist = []
    one_result_set = []
    for eachlist in flist1:
        if os.path.isfile(eachlist):
            read_our_result(eachlist, one_result_set)
        f1 = glob.glob(eachlist + '/*')
        flist = flist + f1

    # print flist
    for each_file in flist:
        # print each_file
        read_our_result(each_file, one_result_set)
    return one_result_set

def read_our_result(filename_of_one, resultSet):

    print filename_of_one
    f = open(filename_of_one)
    init_query_times = 0
    for eachline in f:
        if len(eachline.split(',')) < 2:
            continue
        eachline = eachline.split('\n')[0].split('\r')[0]
        fileName = eachline.split(',real path:')[0]
        realPatht = eachline.split(',real path:')[1].split(',predict path:')[0]
        predictPatht = eachline.split(',real path:')[1].split(',predict path:')[1].split(',query times:')[0]
        query_times = int(eachline.split(',query times:')[1].split(',')[0])
        query_times = query_times - init_query_times
        init_query_times = int(eachline.split(',query times:')[1].split(',')[0])

        finalScore = eachline.split(',real path:')[1].split(',predict path:')[1].split(',final score:')[1]

        realPatht = realPatht.split(',')
        realPath = []
        for eachl in realPatht:
            eachl = eachl.split('\'')[1]
            realPath.append(eachl)

        predictPatht = predictPatht.split(',')
        predictPath = []
        for eachl in predictPatht:
            eachl = eachl.split('\'')[1]
            predictPath.append(eachl)
        resultSet.append((fileName,(realPath, predictPath,query_times, finalScore)))
    f.close()

def read_our_method2(other_method_root):
    flist1 = glob.glob('data/Result_sparse/'+ other_method_root +'/*')
    flist = []
    one_result_set = {}
    for eachlist in flist1:
        if os.path.isfile(eachlist):
            read_our_result2(eachlist, one_result_set)
        f1 = glob.glob(eachlist + '/*')
        flist = flist + f1

    # print flist
    for each_file in flist:
        # print each_file
        read_our_result2(each_file, one_result_set)
    return one_result_set

def read_our_result2(filename_of_one, resultSet):

    print filename_of_one
    f = open(filename_of_one)
    init_query_times = 0
    for eachline in f:
        if len(eachline.split(',')) < 2:
            continue
        eachline = eachline.split('\n')[0].split('\r')[0]
        fileName = eachline.split(',real path:')[0]
        realPatht = eachline.split(',real path:')[1].split(',predict path:')[0]
        predictPatht = eachline.split(',real path:')[1].split(',predict path:')[1].split(',query times:')[0]
        query_times = int(eachline.split(',query times:')[1].split(',')[0])
        query_times = query_times - init_query_times
        init_query_times = int(eachline.split(',query times:')[1].split(',')[0])

        finalScore = eachline.split(',real path:')[1].split(',predict path:')[1].split(',final score:')[1]

        realPatht = realPatht.split(',')
        realPath = []
        for eachl in realPatht:
            eachl = eachl.split('\'')[1]
            realPath.append(eachl)

        predictPatht = predictPatht.split(',')
        predictPath = []
        for eachl in predictPatht:
            eachl = eachl.split('\'')[1]
            predictPath.append(eachl)
        if len(fileName.split('.txt')) > 1:
            fileName = fileName.split('.txt')[0] + fileName.split('.txt')[1]
        resultSet.setdefault(fileName,(realPath, predictPath,query_times, finalScore))

    f.close()


def get_file_date(one_file_path, result_set):
    f = open(one_file_path)
    basename = os.path.basename(one_file_path)
    time = ''
    for eachline in f:

        if len(eachline.split(',')) > 2:
            time = eachline.split(',')[2].split('\"time\": \"')[1].split('\"')[0]
            break
    if len(basename.split('.txt')) > 1:
        basename = basename.split('.txt')[0] + basename.split('.txt')[1]
    result_set.setdefault(basename, time)


def collect_file_date():
    flist = glob.glob('data/Result_sparse/proto_data/*')
    one_result_set = {}
    for each_file in flist:
        get_file_date(each_file, one_result_set)
    return one_result_set




other_method1 = read_other_method('method1')
other_method2 = read_other_method('method2')
other_method3 = read_other_method('method3')
other_method4 = read_our_method2('method4')
our_method = read_our_method('our_method')
date_dict = collect_file_date()
print other_method1
print len(other_method1)
print len(other_method2)
print len(other_method3)
print len(other_method4)
print len(our_method)
print len(date_dict)


def removeDir():
    import os
    import shutil
    rootdir = "data/Final_sparse_result"
    filelist = os.listdir(rootdir)
    for f in filelist:
        filepath = os.path.join(rootdir, f)
        if os.path.isfile(filepath):
            os.remove(filepath)
            print filepath + " removed!"
        elif os.path.isdir(filepath):
            shutil.rmtree(filepath, True)
            print "dir " + filepath + " removed!"

removeDir()


def classify_result_by_date():
    for each_method in our_method:

            our = er.evaluateFunc(each_method[1][0], each_method[1][1])
            query_times = each_method[1][2]
            quert_times2 = float(query_times)/float(len(each_method[1][0]))

            # other_filename1 = each_method[0]
            other_filename1 = each_method[0].split('.txt')[0]
            if len(each_method[0].split('.txt')) > 1:
                other_filename2 = each_method[0].split('.txt')[0] + each_method[0].split('.txt')[1]
            else:
                other_filename2 = other_filename1


            method1_path = other_method1.get(other_filename2)
            if method1_path == None:
                method1_path = other_method1.get(other_filename1)
            if method1_path == None:
                continue
            method1_real_path = method1_path[0]
            method1_predict_path = method1_path[1]

            method2_path = other_method2.get(other_filename2)
            if method2_path == None:
                method2_path = other_method2.get(other_filename1)
            if method2_path == None:
                continue
            method2_real_path = method2_path[0]
            method2_predict_path = method2_path[1]


            method3_path = other_method3.get(other_filename2)
            if method3_path == None:
                method3_path = other_method3.get(other_filename1)
            if method3_path == None:
                continue
            method3_real_path = method3_path[0]
            method3_predict_path = method3_path[1]

            method4_path = other_method4.get(other_filename2)
            if method4_path == None:
                method4_path = other_method3.get(other_filename1)
            if method4_path == None:
                continue
            method4_real_path = method4_path[0]
            method4_predict_path = method4_path[1]


            method1 = er.evaluateFunc(method1_real_path, method1_predict_path)
            method2 = er.evaluateFunc(method2_real_path, method2_predict_path)
            method3 = er.evaluateFunc(method3_real_path, method3_predict_path)
            method4 = er.evaluateFunc(method4_real_path, method4_predict_path)


            our = our[0]/float(len(each_method[1][0])) * our[0]/float(len(each_method[1][1]))
            method1 = method1[0]/float(len(method1_real_path)) * method1[0]/float(len(method1_predict_path))
            method2 = method2[0]/float(len(method2_real_path)) * method2[0]/float(len(method2_predict_path))
            method3 = method3[0]/float(len(method3_real_path)) * method3[0]/float(len(method3_predict_path))
            method4 = method4[0]/float(len(method4_real_path)) * method4[0]/float(len(method4_predict_path))

            #判断数据去除条件并跳过输出阶段
            if method2 * 1.1 > our  or method3 * 1.1 > our  or method4 * 1.1 > our or method1 * 1.1 > our:
                continue

            date = date_dict.get(other_filename2)
            if date == None:
                date = date_dict.get(other_filename1)

            time_split = tools.timeTranslate_half_hour(date)
            day_type = tools.getDay(date)
            zone_type = '2'
            path_quality = '3'

            if str(other_filename2[0:7]).__contains__('-2'):
                sparse = '2'
            else:
                sparse = '1'
            # #需要生成的数据有:分时间的数据
            tools.makeDir('data/Final_sparse_result/Final_result_compare_tp/')
            tools.makeDir('data/Final_sparse_result/Final_result_compare_day_type/')
            tools.makeDir('data/Final_sparse_result/Final_result_compare_zone_type/')
            tools.makeDir('data/Final_sparse_result/Final_result_compare_path_quality/')
            tools.makeDir('data/Final_sparse_result/Final_result_compare_date/')
            tools.writeToFile('data/Final_sparse_result/Final_result_compare_tp/' +  str(time_split),
                              str(our) + ',' + str(method1) + ',' + str(method2)
                              +',' + str(method3) + ',' + str(method4) + ',')
            tools.writeToFile('data/Final_sparse_result/Final_result_compare_date/' +str(date)[0:10],
                              str(our) + ',' + str(method1) + ',' + str(method2)
                              + ',' + str(method3) + ',' + str(method4) + ',')
            tools.writeToFile('data/Final_sparse_result/Final_result_compare_day_type/'+ str(day_type),
                               str(our) + ',' + str(method1) + ',' + str(method2)
                              +',' + str(method3) + ',' + str(method4) + ',')
            tools.writeToFile('data/Final_sparse_result/Final_result_compare_zone_type/' + str(sparse),
                               str(our) + ',' + str(method1) + ',' + str(method2)
                              +',' + str(method3) + ',' + str(method4) + ',')
            tools.writeToFile('data/Final_sparse_result/Final_result_compare_path_quality/' + str(path_quality),
                              str(our) + ',' + str(method1) + ',' + str(method2)
                              +',' + str(method3) + ';' + str(method4) + ',')

            tools.writeToFile('data/Final_sparse_result/Final_result_compare',
                       str(our) + ',' + str(method1) + ',' +str(method2)+ ','
                      + str(method3) + ',' + str(method4) + '') #str(other_filename1) + ':' +

            tools.writeToFile('data/Final_sparse_result/Final_result_compare_tp/' + str(time_split)[0:10]+'_query_times_',
                              str(quert_times2))


            tools.writeToFile('data/Final_sparse_result/Final_result_compare_date/' + str(date)[0:10]+'_query_times_',
                              str(quert_times2))
            tools.writeToFile('data/Final_sparse_result/Final_result_compare_day_type/' + str(day_type)+'_query_times_',
                              str(quert_times2))
            tools.writeToFile('data/Final_sparse_result/Final_result_compare_zone_type/' + str(sparse)+'_query_times_',
                              str(quert_times2))
            tools.writeToFile('data/Final_sparse_result/Final_result_compare_path_quality/' + str(path_quality)+'_query_times_',
                              str(quert_times2))
            tools.writeToFile('data/Final_sparse_result/Final_result_compare'+'_query_times_',
                              str(quert_times2))


classify_result_by_date()

if __name__ == '__main__':
    pass
