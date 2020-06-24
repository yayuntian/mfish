#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import json
import time
import copy
import requests
from requests.auth import HTTPBasicAuth

auth = HTTPBasicAuth('admin', 'Harbor12345')

harbor_url = 'yhub.ssl.ysten.com'
# harbor_url = 'yhub-154.ssl.ysten.com:9881'
api_url = 'https://' + harbor_url + '/api/'

project_list = [
    'anhui',
    'beijing',
    'chongqing',
    # 'dev',
    'fujian',
    'guangdong',
    'guangxi',
    'guizhou',
    'hainan',
    'heilongjiang',
    'hunan',
    # 'inf-base',
    # 'inf-dev',
    'jiangsu',
    'jiangxi',
    'jiangxijk',
    'liaoning',
    'ningxia',
    'public',
    'sichuan',
    'wxcenter',
    # 'ycs',
    'yiban',
    'zhejiang',
    # 'release'
]

harbor_list = [
    {
        "name": "公网",
        "ename": "public",
        "url": "https://yhub-public.ssl.ysten.com:8880",
        "key": "admin",
        "secret": "Yhub123qwe"
    },
    {
        "name": "重庆",
        "ename": "chongqing",
        "url": "https://yhub-cq.ssl.ysten.com:9881",
        "key": "sync",
        "secret": "ystHaCqSync123#$%"
    },
    {
        "name": "浙江",
        "ename": "zhejiang",
        "url": "http://zhejiang.yhub.ysten.com:8089",
        "key": "sync",
        "secret": "YstenSync123456"
    },
    {
        "name": "辽宁",
        "ename": "liaoning",
        "url": "https://ln.yhub.ysten.com:9881",
        "key": "sync",
        "secret": "lnSync123@ysten.com"
    },
    {
        "name": "四川",
        "ename": "sichuan",
        "url": "http://sc.yhub.ysten.com:9881",
        "key": "sync",
        "secret": "YzcyYTQ4YjExOTAx"
    },
    {
        "name": "福建",
        "ename": "fujian",
        "url": "https://yhub-fj.ssl.ysten.com:9881",
        "key": "sync",
        "secret": "Cmfjyhub1234"
    },
    {
        "name": "无锡中心",
        "ename": "wxcenter",
        "url": "https://yhub-center.ssl.ysten.com:9880",
        "key": "sync",
        "secret": "CMWXsync321#@!"
    },
    {
        "name": "黑龙江",
        "ename": "heilongjiang",
        "url": "https://yhub-hlj.ssl.ysten.com:9881",
        "key": "sync",
        "secret": "Cmhljyhub1234"
    },
    {
        "name": "江西",
        "ename": "jiangxi",
        "url": "https://yhub-jx.ssl.ysten.com:9881",
        "key": "cmjxsync",
        "secret": "CMJXsync321#@!"
    },
    {
        "name": "广西",
        "ename": "guangxi",
        "url": "https://yhub-gx.ssl.ysten.com:9881",
        "key": "sync",
        "secret": "Gx@#$1122.."
    },
    {
        "name": "贵州",
        "ename": "guizhou",
        "url": "https://yhub-gz.ssl.ysten.com:9881",
        "key": "sync",
        "secret": "Ysten@sync123$"
    },
    {
        "name": "大数据",
        "url": "http://registry.bigdata.ysten.com",
        "key": "admin",
        "secret": "Harbor12345"
    },
    {
        "name": "江苏",
        "ename": "jiangsu",
        "url": "https://yhub-js.ssl.ysten.com:9881",
        "key": "sync",
        "secret": "D%kTjS734KIWhie9"
    },
    {
        "name": "北京",
        "ename": "beijing",
        "url": "https://yhub-bj.ssl.ysten.com:9881",
        "key": "sync",
        "secret": "Cmbjyhub1234"
    },
    {
        "name": "安徽",
        "ename": "anhui",
        "url": "https://yhub-ah.ssl.ysten.com:8088",
        "key": "sync",
        "secret": "rzxlSzy@0519Ykbjkyd"
    },
    {
        "name": "宁夏",
        "ename": "ningxia",
        "url": "https://yhub-nx.ssl.ysten.com:9881",
        "key": "sync",
        "secret": "Ysten@sync123$"
    },
    {
        "name": "云南",
        "ename": "yunnan",
        "url": "https://yhub-yn.ssl.ysten.com:9881",
        "key": "sync",
        "secret": "Hp110@Cmyn!ni%ce"
    },
    {
        "name": "湖南",
        "ename": "hunan",
        "url": "https://yhub-hn.ssl.ysten.com:9881",
        "key": "sync",
        "secret": "Ysten@sync123$"
    },
    {
        "name": "海南",
        "ename": "hainan",
        "url": "https://yhub-hi.ssl.ysten.com:9881",
        "key": "sync",
        "secret": "Ysten@123"
    },
    {
        "name": "山西",
        "ename": "shanxi",
        "url": "https://yhub-sx.ssl.ysten.com",
        "key": "admin",
        "secret": "Harbor12345"
    },
    {
        "name": "怡伴",
        "ename": "yiban",
        "url": "https://yhub-yb.ssl.ysten.com:8088",
        "key": "sync",
        "secret": "Ysten@2019"
    },
    {
        "name": "newTV",
        "ename": "newtv",
        "url": "http://123.206.7.55:8088",
        "key": "sync",
        "secret": "Ysten@2019"
    },
    {
        "name": "广东",
        "ename": "guangdong",
        "url": "http://183.240.170.27:8880",
        "key": "gdiptv",
        "secret": "GDYsten123"
    },
    {
        "name": "辽宁-IPTV",
        "ename": "liaoning-iptv",
        "url": "https://yhub.lnitv.com:9998",
        "key": "sync",
        "secret": "YhubLnitvCom2019"
    }
]

registries_list = [
    {
        "id": 20,
        "name": "海南",
        "description": "",
        "type": "harbor",
        "url": "https://yhub-hi.ssl.ysten.com:9881",
        "token_service_url": "",
        "credential": {
            "type": "basic",
            "access_key": "sync",
            "access_secret": "*****"
        },
        "insecure": False,
        "status": "healthy",
        "creation_time": "2020-05-27T08:03:40.410726Z",
        "update_time": "2020-05-27T08:15:32.34248Z"
    },
    {
        "id": 21,
        "name": "怡伴",
        "description": "",
        "type": "harbor",
        "url": "https://yhub-yb.ssl.ysten.com:8088",
        "token_service_url": "",
        "credential": {
            "type": "basic",
            "access_key": "sync",
            "access_secret": "*****"
        },
        "insecure": False,
        "status": "healthy",
        "creation_time": "2020-05-27T08:03:45.876205Z",
        "update_time": "2020-05-27T08:15:32.861045Z"
    },
    {
        "id": 22,
        "name": "newTV",
        "description": "",
        "type": "harbor",
        "url": "http://123.206.7.55:8088",
        "token_service_url": "",
        "credential": {
            "type": "basic",
            "access_key": "sync",
            "access_secret": "*****"
        },
        "insecure": False,
        "status": "healthy",
        "creation_time": "2020-05-27T08:03:47.091468Z",
        "update_time": "2020-05-27T08:15:33.002857Z"
    },
    {
        "id": 5,
        "name": "公网",
        "description": "",
        "type": "harbor",
        "url": "https://yhub-public.ssl.ysten.com:8880",
        "token_service_url": "",
        "credential": {
            "type": "basic",
            "access_key": "admin",
            "access_secret": "*****"
        },
        "insecure": False,
        "status": "healthy",
        "creation_time": "2020-05-27T07:59:19.784261Z",
        "update_time": "2020-05-27T08:15:33.431763Z"
    },
    {
        "id": 6,
        "name": "重庆",
        "description": "",
        "type": "harbor",
        "url": "https://yhub-cq.ssl.ysten.com:9881",
        "token_service_url": "",
        "credential": {
            "type": "basic",
            "access_key": "sync",
            "access_secret": "*****"
        },
        "insecure": False,
        "status": "healthy",
        "creation_time": "2020-05-27T07:59:20.301612Z",
        "update_time": "2020-05-27T08:15:33.874206Z"
    },
    {
        "id": 7,
        "name": "浙江",
        "description": "",
        "type": "harbor",
        "url": "http://zhejiang.yhub.ysten.com:8089",
        "token_service_url": "",
        "credential": {
            "type": "basic",
            "access_key": "sync",
            "access_secret": "*****"
        },
        "insecure": False,
        "status": "healthy",
        "creation_time": "2020-05-27T07:59:20.49406Z",
        "update_time": "2020-05-27T08:15:34.110191Z"
    },
    {
        "id": 17,
        "name": "安徽",
        "description": "",
        "type": "harbor",
        "url": "https://yhub-ah.ssl.ysten.com:8088",
        "token_service_url": "",
        "credential": {
            "type": "basic",
            "access_key": "sync",
            "access_secret": "*****"
        },
        "insecure": False,
        "status": "healthy",
        "creation_time": "2020-05-27T08:02:34.799633Z",
        "update_time": "2020-05-27T08:15:38.440047Z"
    },
    {
        "id": 13,
        "name": "广西",
        "description": "",
        "type": "harbor",
        "url": "https://yhub-gx.ssl.ysten.com:9881",
        "token_service_url": "",
        "credential": {
            "type": "basic",
            "access_key": "sync",
            "access_secret": "*****"
        },
        "insecure": False,
        "status": "healthy",
        "creation_time": "2020-05-27T08:01:23.655582Z",
        "update_time": "2020-05-27T08:20:31.609735Z"
    },
    {
        "id": 14,
        "name": "贵州",
        "description": "",
        "type": "harbor",
        "url": "https://yhub-gz.ssl.ysten.com:9881",
        "token_service_url": "",
        "credential": {
            "type": "basic",
            "access_key": "sync",
            "access_secret": "*****"
        },
        "insecure": False,
        "status": "healthy",
        "creation_time": "2020-05-27T08:01:25.145499Z",
        "update_time": "2020-05-27T08:20:32.039067Z"
    },
    {
        "id": 8,
        "name": "四川",
        "description": "",
        "type": "harbor",
        "url": "http://sc.yhub.ysten.com:9881",
        "token_service_url": "",
        "credential": {
            "type": "basic",
            "access_key": "sync",
            "access_secret": "*****"
        },
        "insecure": False,
        "status": "healthy",
        "creation_time": "2020-05-27T08:01:16.177425Z",
        "update_time": "2020-05-27T08:15:34.532403Z"
    },
    {
        "id": 9,
        "name": "福建",
        "description": "",
        "type": "harbor",
        "url": "https://yhub-fj.ssl.ysten.com:9881",
        "token_service_url": "",
        "credential": {
            "type": "basic",
            "access_key": "sync",
            "access_secret": "*****"
        },
        "insecure": False,
        "status": "healthy",
        "creation_time": "2020-05-27T08:01:17.769302Z",
        "update_time": "2020-05-27T08:15:35.023844Z"
    },
    {
        "id": 10,
        "name": "无锡中心",
        "description": "",
        "type": "harbor",
        "url": "https://yhub-center.ssl.ysten.com:9880",
        "token_service_url": "",
        "credential": {
            "type": "basic",
            "access_key": "sync",
            "access_secret": "*****"
        },
        "insecure": False,
        "status": "healthy",
        "creation_time": "2020-05-27T08:01:19.023654Z",
        "update_time": "2020-05-27T08:15:35.260897Z"
    },
    {
        "id": 11,
        "name": "黑龙江",
        "description": "",
        "type": "harbor",
        "url": "https://yhub-hlj.ssl.ysten.com:9881",
        "token_service_url": "",
        "credential": {
            "type": "basic",
            "access_key": "sync",
            "access_secret": "*****"
        },
        "insecure": False,
        "status": "healthy",
        "creation_time": "2020-05-27T08:01:20.598462Z",
        "update_time": "2020-05-27T08:15:35.810695Z"
    },
    {
        "id": 15,
        "name": "江苏",
        "description": "",
        "type": "harbor",
        "url": "https://yhub-js.ssl.ysten.com:9881",
        "token_service_url": "",
        "credential": {
            "type": "basic",
            "access_key": "sync",
            "access_secret": "*****"
        },
        "insecure": False,
        "status": "healthy",
        "creation_time": "2020-05-27T08:02:27.558138Z",
        "update_time": "2020-05-27T08:20:32.223844Z"
    },
    {
        "id": 23,
        "name": "辽宁-IPTV",
        "description": "",
        "type": "harbor",
        "url": "https://yhub.lnitv.com:9998",
        "token_service_url": "",
        "credential": {
            "type": "basic",
            "access_key": "sync",
            "access_secret": "*****"
        },
        "insecure": False,
        "status": "healthy",
        "creation_time": "2020-05-27T08:04:49.98682Z",
        "update_time": "2020-05-27T08:20:32.649481Z"
    },
    {
        "id": 16,
        "name": "北京",
        "description": "",
        "type": "harbor",
        "url": "https://yhub-bj.ssl.ysten.com:9881",
        "token_service_url": "",
        "credential": {
            "type": "basic",
            "access_key": "sync",
            "access_secret": "*****"
        },
        "insecure": False,
        "status": "healthy",
        "creation_time": "2020-05-27T08:02:33.192529Z",
        "update_time": "2020-05-27T08:20:32.973011Z"
    },
    {
        "id": 18,
        "name": "宁夏",
        "description": "",
        "type": "harbor",
        "url": "https://yhub-nx.ssl.ysten.com:9881",
        "token_service_url": "",
        "credential": {
            "type": "basic",
            "access_key": "sync",
            "access_secret": "*****"
        },
        "insecure": False,
        "status": "healthy",
        "creation_time": "2020-05-27T08:02:36.334391Z",
        "update_time": "2020-05-27T08:20:33.431496Z"
    },
    {
        "id": 19,
        "name": "湖南",
        "description": "",
        "type": "harbor",
        "url": "https://yhub-hn.ssl.ysten.com:9881",
        "token_service_url": "",
        "credential": {
            "type": "basic",
            "access_key": "sync",
            "access_secret": "*****"
        },
        "insecure": False,
        "status": "healthy",
        "creation_time": "2020-05-27T08:03:38.828597Z",
        "update_time": "2020-05-27T08:20:34.074425Z"
    },
    {
        "id": 12,
        "name": "江西",
        "description": "",
        "type": "harbor",
        "url": "https://yhub-jx.ssl.ysten.com:9881",
        "token_service_url": "",
        "credential": {
            "type": "basic",
            "access_key": "cmjxsync",
            "access_secret": "*****"
        },
        "insecure": False,
        "status": "healthy",
        "creation_time": "2020-05-27T08:01:21.934115Z",
        "update_time": "2020-05-27T08:15:36.04731Z"
    }
]

sync_list = [
    # {
    #     "project": "ycs/**"
    # },
    # {
    #     "project": "inf-base/**"
    # },
    {
        "project": "anhui/**",
        "dest_region": "安徽",
    },
    {
        "project": "beijing/**",
        "dest_region": "北京",
    },
    {
        "project": "chongqing/**",
        "dest_region": "重庆",
    },
    {
        "project": "fujian/**",
        "dest_region": "福建",
    },
    {
        "project": "guangdong/**",
        "dest_region": "广东",
    },
    {
        "project": "guangxi/**",
        "dest_region": "广西",
    },
    {
        "project": "guizhou/**",
        "dest_region": "贵州",
    },
    {
        "project": "heilongjiang/**",
        "dest_region": "黑龙江",
    },
    {
        "project": "hainan/**",
        "dest_region": "海南",
    },    {
        "project": "hunan/**",
        "dest_region": "湖南",
    },
    {
        "project": "jiangsu/**",
        "dest_region": "江苏",
    },    {
        "project": "jiangxi/**",
        "dest_region": "江西",
    },
    {
        "project": "jiangxijk/**",
        "dest_region": "江西",
    },
    {
        "project": "liaoning/**",
        "dest_region": "辽宁-IPTV",
    },
    {
        "project": "ningxia/**",
        "dest_region": "宁夏",
    },
    {
        "project": "public/**",
        "dest_region": "公网",
    },
    {
        "project": "sichuan/**",
        "dest_region": "四川",
    },
    {
        "project": "wxcenter/**",
        "dest_region": "无锡中心",
    },
    {
        "project": "yiban/**",
        "dest_region": "怡伴",
    },
    {
        "project": "zhejiang/**",
        "dest_region": "浙江",
    }
]


# 获取同步时需要的目的仓库地址信息
def make_dest_registry():
    harbor_dict = {}
    registries_dict = {}
    for hb in harbor_list:
        harbor_dict[hb['name']] = hb

    for reg in registries_list:
        reg['credential']['access_secret'] = harbor_dict[reg['name']]['secret']
        reg['ename'] = harbor_dict[reg['name']]['ename']
        registries_dict[reg['name']] = reg
        print(reg)

    # print(json.dumps(harbor_dict, ensure_ascii=False, indent=2))
    # print(json.dumps(registries_dict, ensure_ascii=False, indent=2))

    # print(harbor_dict['公网'])
    # print(registries_dict['公网'])

    return registries_dict


def list_image():
    f = open('images_bak.txt', 'a')

    r_project_id = requests.get(url=api_url + 'projects?', auth=auth)
    list_project_id = r_project_id.json()
    if r_project_id.content:
        print(len(list_project_id))
        for i in range(len(list_project_id)):
            pname = list_project_id[i]['name']
            # print(pname)

            project_id = list_project_id[i]['project_id']
            r_project_name = requests.get(
                url=api_url + 'repositories?project_id=' + str(project_id), auth=auth)
            list_project_name = r_project_name.json()
            if r_project_name.content:
                # print(len(list_project_name))
                for j in range(len(list_project_name)):
                    project_name = list_project_name[j]['name']
                    r_tag_name = requests.get(
                        url=api_url + 'repositories/' + project_name + '/tags?detail=1', auth=auth)
                    # time.sleep(0.1)
                    while r_tag_name.status_code != 200:
                        time.sleep(1)
                        r_tag_name = requests.get(
                            url=api_url + 'repositories/' + project_name + '/tags?detail=1', auth=auth)
                        # time.sleep(0.1)
                    list_tag_name = r_tag_name.json()
                    for k in range(len(list_tag_name)):
                        tag_name = list_tag_name[k]['name']
                        image_name = project_name + ':' + tag_name
                        print(harbor_url + '/' + image_name)
                        f.writelines('\n' + image_name)

    f.close()


def add_project():
    obj = {
        "project_name": "dev",
        "metadata": {
            "public": "false"
        },
        "count_limit": -1,
        "storage_limit": -1
    }

    for reg in project_list:
        obj['project_name'] = reg + '-dev'
        print(json.dumps(obj))
        req = requests.post(api_url + 'projects', data=json.dumps(obj), auth=auth)
        print(req.status_code, req.text)


def add_harbor():
    # https://yhub.ssl.ysten.com/api/registries

    obj = {
        "credential": {
            "access_key": "sync",
            "access_secret": "ystHaCqSync123#$%",
            "type": "basic"
        },
        "description": "",
        "insecure": False,
        "name": "重庆harbor",
        "type": "harbor",
        "url": "https://yhub-cq.ssl.ysten.com:9881"
    }

    count = 1
    for reg in harbor_list:
        obj['name'] = reg['name']
        obj['url'] = reg['url']
        obj['credential']['access_key'] = reg['key']
        obj['credential']['access_secret'] = reg['secret']

        # print(count, json.dumps(obj, ensure_ascii=False, indent=2))
        count = count + 1
        req = requests.post(api_url + 'registries', data=json.dumps(obj).encode('utf-8'), auth=auth)
        if req.status_code == 504:
            print('### 检查core.log日志，通常是远程仓库不可达')
        print(req.status_code, req.content.decode('utf-8'))


def get_sync():
    # https://yhub.ssl.ysten.com/api/replication/policies

    req = requests.get(api_url + 'replication/policies', auth=auth)
    if req.status_code == 504:
        print('### 检查core.log日志，通常是远程仓库不可达')

    return json.loads(req.content.decode('utf-8'))


def del_sync():
    polis = get_sync()

    ret_list = []
    for po in polis:
        if 'dev' in po['name']:
            ret_list.append(po)
            print(po)

    for ret in ret_list:
        req = requests.delete(api_url + 'replication/policies/' + str(ret['id']), auth=auth)
        if req.status_code == 504:
            print('### 检查core.log日志，通常是远程仓库不可达')
        print(req.status_code, req.content.decode('utf-8'))


def add_sync():
    # https://yhub.ssl.ysten.com/api/replication/policies
    # manual
    # event_based
    registries_dict = make_dest_registry()
    obj_list = []
    obj = {
        "name": "ycs2public",
        "description": None,
        "src_registry": None,
        "dest_registry": None,
        "dest_namespace": None,
        "trigger": {
            "type": "event_based",
            "trigger_settings": {
                "cron": ""
            }
        },
        "deletion": True,
        "enabled": True,
        "override": True,
        "filters": [
            {
                "type": "name",
                "value": "ycs/**"
            }
        ]
    }

    for sync in sync_list:
        pro = sync['project']
        # name = pro.split('/')[0]
        name = pro.split('/')[0] + '-dev'
        if 'dest_region' in sync.keys():
            if sync['dest_region'] not in registries_dict.keys():
                print('### 地区不存在 ->', sync['dest_region'])
                continue

            obj['name'] = name + '2' + registries_dict[sync['dest_region']]['ename'] + '-dev'
            obj['dest_registry'] = registries_dict[sync['dest_region']]
            # obj['filters'][0]['value'] = pro + '-dev'
            obj['filters'][0]['value'] = pro.split('/')[0] + '-dev/' + pro.split('/')[1]

            tmp = copy.deepcopy(obj)
            obj_list.append(tmp)
        else:
            # print('全国同步项目')
            for reg in registries_list:
                obj['name'] = name + '2' + registries_dict[reg['name']]['ename']
                obj['dest_registry'] = registries_dict[reg['name']]
                obj['filters'][0]['value'] = pro

                tmp = copy.deepcopy(obj)
                obj_list.append(tmp)

    print(json.dumps(obj_list, ensure_ascii=False, indent=2))

    for obj in obj_list:
        # print(json.dumps(obj, ensure_ascii=False, indent=2))
        req = requests.post(api_url + 'replication/policies', data=json.dumps(obj).encode('utf-8'), auth=auth)
        if req.status_code == 504:
            print('### 检查core.log日志，通常是远程仓库不可达')
        print(req.status_code, req.content.decode('utf-8'))




if __name__ == '__main__':
    # list_image()
    # add_project()
    # add_harbor()
    # make_dest_registry()
    add_sync()
    # get_sync()
    # del_sync()