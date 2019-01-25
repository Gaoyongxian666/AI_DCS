# -*- coding: utf-8 -*-

"""

__title__ = ''

__author__ = 'g1695'

__mtime__ = '2018/12/2'

"""

from AIDCS.tasks import do_painter,add,do_ink,do_sketch,do_figure,do_style

do_sketch.delay("/home/ai/AI_DCS/AIDCS/input/77.png","/home/ai/AI_DCS/AIDCS/sk.jpg")
do_painter.delay("/home/ai/AI_DCS/AIDCS/input/1.png","/home/ai/AI_DCS/AIDCS/pa.jpg")
do_style.delay("/home/ai/AI_DCS/AIDCS/input/nature_image.jpg","/home/ai/AI_DCS/AIDCS/st.jpg")
do_figure.delay("/home/ai/AI_DCS/AIDCS/input/nature_image.jpg","/home/ai/AI_DCS/AIDCS/fi.jpg")
do_ink.delay("/home/ai/AI_DCS/AIDCS/input/gray.jpg","/home/ai/AI_DCS/AIDCS/gray.jpg")
#add.delay(4,4)