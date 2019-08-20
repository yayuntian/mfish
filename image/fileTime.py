# -*- coding:utf-8 -*-

import shutil
import os
import time
import exifread
import random

suffix = ('.gif', '.jpg', '.jpeg', '.png', '.bmp', '.svg')


class ReadFailException(Exception):
    pass


def getOriginalDate(filename):
    try:
        fd = open(filename, 'rb')
    except:
        raise ReadFailException("unopen file[%s]\n" % filename)
    data = exifread.process_file(fd)
    if data:
        try:
            t = data['EXIF DateTimeOriginal']
            # return str(t).replace(":", ".").replace(" ", "_")
        except:
            pass
    state = os.stat(filename)
    return time.strftime("%Y.%m.%d_%H.%M.%S", time.localtime(state[-2]))


def classifyPictures(path):
    count = 0
    for root, dirs, files in os.walk(path, True):
        dirs[:] = []
        for f in files:
            filename = os.path.join(root, f)
            ext = os.path.splitext(f)[1].lower()
            if ext not in suffix:
                continue
            info = "文件名: " + filename + " "
            t = ""
            try:
                t = getOriginalDate(filename)
            except Exception as e:
                print(e)
                continue
            info = info + "拍摄时间：" + t + " "
            pwd = root + '\\' + t[:7]
            dst = pwd + '\\' + t.replace(".", "")
            if not os.path.exists(pwd):
                os.mkdir(pwd)
            if os.path.exists(dst + ext):
                dst += "_" + str(random.randint(1, 100))
            dst += ext

            count += 1
            print(count, info, dst)
            try:
                shutil.copy2(filename, dst)
                os.remove(filename)
            except Exception as e:
                print(e)
                continue


if __name__ == "__main__":
    path = 'D:/beifen/2002.12'
    classifyPictures(path)