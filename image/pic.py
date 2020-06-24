#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import os
import exifread
from datetime import datetime
from PIL import Image
import time


VOLPATH = "/Volumes/F/百度云同步盘/来自：iPhone/"


def imgDate(fn):
    "returns the image date from image (if available)\nfrom Orthallelous"
    std_fmt = '%Y:%m:%d %H:%M:%S.%f'
    # for subsecond prec, see doi.org/10.3189/2013JoG12J126 , sect. 2.2, 2.3
    tags = [(36867, 37521),  # (DateTimeOriginal, SubsecTimeOriginal)
            (36868, 37522),  # (DateTimeDigitized, SubsecTimeOriginal)
            (306, 37520), ]  # (DateTime, SubsecTime)
    exif = Image.open(fn)._getexif()
    print(exif)




def main(file):
    # im = Image.open(file)
    # print(im._getexif())

    f = open(file, 'rb')
    tags = exifread.process_file(f)

    # print('拍摄时间：', tags['EXIF DateTimeOriginal'])

    for tag in tags.keys():
        print("Key: {}, value {}".format(tag, tags[tag]))


if __name__ == '__main__':
    # main('/Users/eric/Downloads/20091003_164142.jpg')
    imgDate('/Users/eric/Downloads/20091003_164142.jpg')
