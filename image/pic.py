# -*- coding:utf-8 -*-

import hashlib
import logging
import os

import redis
from PIL import Image

suffix = ('.gif', '.jpg', '.jpeg', '.png', '.bmp', '.svg')

# g = os.walk('D:\\备份\\nanjing')
g = os.walk('D:\\备份')
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

            print(count, fname)
            m = md5(fname)
            if r.exists(m):
                ex = r.get(m).decode("utf-8")
                tmp = fname
                if len(ex) > len(fname):
                    tmp = fname
                else:
                    tmp = ex
                if os.path.exists(tmp):
                    os.remove(tmp)
                    logging.warning("remove %s", tmp)
                    continue
            r.set(m, fname)


def imageInfo(fname):
    img = Image.open(fname)
    width, height = img.size
    print(width, height)


if __name__ == "__main__":
    r.flushdb()
    list()