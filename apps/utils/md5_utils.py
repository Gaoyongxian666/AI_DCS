# -*- coding: utf-8 -*-

"""

__title__ = ''

__author__ = 'g1695'

__mtime__ = '2018/10/7'

"""

import hashlib
import os


def get_md5_01(file_path):
    md5 = None
    if os.path.isfile(file_path):
        f = open(file_path, 'rb')
        md5_obj = hashlib.md5()
        md5_obj.update(f.read())
        hash_code = md5_obj.hexdigest()
        f.close()
        md5 = str(hash_code).lower()
    return md5
def get_md5_02(file):
    md5 = None
    f = file
    md5_obj = hashlib.md5()
    md5_obj.update(f.read())
    hash_code = md5_obj.hexdigest()
    f.close()
    md5 = str(hash_code).lower()
    return md5


if __name__ == "__main__":
    file_path = r'D:\Python_project\Django\AI_DCS\media\works\2018\10\logo_dZQMlXb.png'
    md5_01 = get_md5_01(file_path)
    print(md5_01)
    # 947671c4d596a670e7b7d3e5abe23847
    # 947671c4d596a670e7b7d3e5abe23847