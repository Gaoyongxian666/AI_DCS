# -*- coding: utf-8 -*-

"""

__title__ = ''

__author__ = 'g1695'

__mtime__ = '2019/5/17'

"""
from AIDCS.tasks import do_style

#do_ink.delay("/home/ai/AI_DCS/AIDCS/input/gray.jpg","/home/ai/AI_DCS/AIDCS/gray.jpg")
#add.delay(4,4)
result=do_style.delay(content="/home/ai/Github/AIDCS/input/10.png",output="/home/ai/Github/AI_DCS/output.jpg",style_model='/home/ai/Github/AIDCS/StyleTransfer/models/wave.ckpt')
print(result)
