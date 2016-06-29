#-*- coding: UTF-8 -*-
'''
@author: chenwuji
Test pycompute
'''

from odps import ODPS
odps = ODPS('XoDqd4UUqEIjLody', 'xE4w9YrxDyBhQDUjxmqDpxsKDiMtEW', 'prj_tc_30372_fbe90157126d',
            endpoint='http://service.odps.aliyun.com/api')
project = odps.get_project()              # 取到默认项目
for table in odps.list_tables():
    print table