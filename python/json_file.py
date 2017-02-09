#!/usr/bin/env python
import json


num = 0
f = open('/tmp/http.json','r')
for x in f:
    #print(num,x)
    line = x.strip().decode('utf-8')
    line = line.strip(',')
    #print(num, line)
    js = json.loads(line)
    #print(num, js)

    num += 1
f.close()
