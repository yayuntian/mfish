# -*- coding:utf-8 -*-

import os
import hashlib
import redis
from PIL import Image
import shutil
import logging


suffix = ('.gif', '.jpg', '.jpeg', '.png', '.bmp', '.svg')

# g = os.walk('D:\\备份\\nanjing')
g = os.walk('D:\\备份')
dup = 'D:\\dup'
min_dir_512 = 'D:\\512k'
min_dir_1024 = 'D:\\1024k'
min_dir_256 = 'D:\\256k'
r = redis.Redis(host='192.168.12.53', port=6379, db=1)

logging.basicConfig(level=logging.INFO,
                    filename='./log.txt',
                    filemode='w',
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def list():
    count = 0
    for path, dir, file in g:
        print("==============", path, dir, "=============");
        for f in file:
            fname = os.path.join(path, f)
            if f.startswith(".") or os.path.splitext(f)[1].lower() not in suffix:
                print("ingore file: ", fname)
                logging.info("ignore file: %s", fname)
                continue
            count += 1

            size = os.path.getsize(fname) / 1024
            print(count, fname, size)
            # logging.info("%d \t %s", count, fname)

            if size < 256:
                if os.path.exists(os.path.join(min_dir_256, f)):
                    os.remove(fname)
                    logging.warning("remove %s", fname)
                    continue
                logging.warning("move lt 256k file: %s", fname)
                shutil.move(fname, min_dir_256)
                continue

            if size < 512:
                if os.path.exists(os.path.join(min_dir_512, f)):
                    os.remove(fname)
                    logging.warning("remove %s", fname)
                    continue
                logging.warning("move lt 512k file: %s", fname)
                shutil.move(fname, min_dir_512)
                continue

            if size < 1024:
                if os.path.exists(os.path.join(min_dir_1024, f)):
                    os.remove(fname)
                    logging.warning("remove %s", fname)
                    continue
                logging.warning("move lt 1024k file: %s", fname)
                shutil.move(fname, min_dir_1024)
                continue


            m = md5(fname)
            if r.exists(m):
                ex = r.get(m).decode("utf-8")
                # print("####################### file dup:", ex, fname)
                tmp = fname
                if len(ex) > len(fname):
                    tmp = fname
                else:
                    tmp = ex
                if os.path.exists(tmp):
                    if os.path.exists(os.path.join(dup, f)):
                        os.remove(tmp)
                        logging.warning("remove %s", tmp)
                        continue
                    logging.warning("move file: %s", tmp)
                    shutil.move(tmp, dup)
                continue
            r.set(m, fname)


def imageInfo(fname):
    img = Image.open(fname)
    width, height = img.size
    print(width, height)


if __name__ == "__main__":
    r.flushdb()
    list()