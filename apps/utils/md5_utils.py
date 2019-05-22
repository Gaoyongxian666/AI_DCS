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
def get_works(all_works):
    all_works_ = []
    md5 = "ec1d1b1554a049dad66ea68a306bfe1e"
    # 比较 md5 值判断是否显示
    # md5="ec1d1b1554a049dad66ea68a306bf1e"
    for all_work in all_works:
        image_path = all_work.image.path
        img_md5 = get_md5_01(image_path)
        if md5 == img_md5:
            continue
        all_works_.append(all_work)
    return all_works_


if __name__ == "__main__":
    file_path = r'D:\Python_project\Django\AI_DCS\media\works\2018\10\logo_dZQMlXb.png'
    md5_01 = get_md5_01(file_path)
    print(md5_01)
    # 947671c4d596a670e7b7d3e5abe23847
    # 947671c4d596a670e7b7d3e5abe23847