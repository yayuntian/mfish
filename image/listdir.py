#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os



VOLPATH_IP = "/Volumes/F/百度云同步盘/来自：iPhone/"
VOLPATH_BF = "/Volumes/F/百度云同步盘/备份/"
VOLPATH = "/Volumes/F/百度云同步盘/"

DOWNLOAD = "/Users/eric/Downloads/img"



vol_list = []


def removeFile(file):
    try:
        os.remove(file)
    except FileNotFoundError:
        print("No such file or directory:" + file)
        return
    else:
      print("remove file: %s" % file)

# 遍历文件夹
def walkFile(file):
    file_count = 0
    for root, dirs, files in os.walk(file):
        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list

        # 遍历文件
        for f in files:
            file_count = file_count + 1
            pic = os.path.join(root, f)
            # print(pic)
            vol_list.append(pic)

        # 遍历所有的文件夹
        # for d in dirs:
        #     print(os.path.join(root, d))

    print("Total file %d" % file_count)
    # for x in vol_list:
    #     print(x)
    # print("Total file %d" % file_count)


def dupPic(file):
    file_count = 0
    for root, dirs, files in os.walk(file):
        for f in files:
            # print(f)

            for x in vol_list:
                if x.endswith(f) == True:
                    file_count = file_count + 1
                    print("dup file:", x)
                    removeFile(x)

    print('Total remove file count: ', file_count)


def main():
    walkFile(VOLPATH)
    dupPic(DOWNLOAD)


if __name__ == '__main__':
    main()
