# -*- encoding: utf-8 -*-
import json
import os
from configparser import ConfigParser, RawConfigParser
from shenqioperate.settings import BASE_DIR
"""封装获取配置的方法"""


def getZoneArray():
    # 获取ZoneArray
    # return dict
    configpath = os.path.join(BASE_DIR, 'configure\zonelist.ini')
    cp = ConfigParser()
    cp.read(configpath, encoding='utf-8')
    zonearray_str = cp.get('zonelist', "ZoneArray")
    zonearray_list = json.loads(zonearray_str)  # 将列表字符串转成列表

    zonearray = {}
    for i in zonearray_list:
        pt = i['id']
        pn = i['zone']
        dict = {pt: pn}
        zonearray.update(dict)
    # print(zonearray)
    # print(type(zonearray))
    return zonearray


def getemailUrl():
    # 获取emailUrl
    # return dict
    configpath = os.path.join(BASE_DIR, 'configure\zonelist.ini')
    cp = ConfigParser()
    cp.read(configpath, encoding='utf-8')
    emailUrl_str = cp.get('zonelist', "emailUrl")
    # print(emailUrl_str)
    # print(type(emailUrl_str))
    emailUrl_dict = json.loads(emailUrl_str)
    return emailUrl_dict


def getzoneStatusUrl():
    # 获取zoneStatusUrl
    configpath = os.path.join(BASE_DIR, 'configure\zonelist.ini')
    cp = ConfigParser()
    cp.read(configpath, encoding='utf-8')
    zoneStatusUrl_str = cp.get('zonelist', 'zoneStatusUrl')
    return zoneStatusUrl_str


def getplatformAccessArray():
    # 获取platformAccessArray
    # return list
    configpath = os.path.join(BASE_DIR, 'configure\zonelist.ini')
    cp = ConfigParser()
    cp.read(configpath, encoding='utf-8')
    platformAccessArray_str = cp.get('zonelist', 'platformAccessArray')
    platformAccessArray_list = json.loads(platformAccessArray_str)

    return platformAccessArray_list
    # platformParams = {}
    # param = {}
    # for i in platformAccessArray_list:
    #     childList = i['childList']
    #     for j in childList:
    #         pt = j['child_platform_type']
    #         pn = j['child_platform_name']
    #         if pt == key:
    #             dict = {pt: pn}
    #             param.update(dict)
    # # print(platformParams)
    # print(param)
    # return param


def getdbconfig(bdconfig):
    configpath = os.path.join(BASE_DIR, 'configure\DBconfig.ini')
    rp = RawConfigParser()  # 由于配置中含有%，需要换成此方法
    rp.read(configpath, encoding='utf-8')
    dbconfig_str = rp.get('dbconfig', bdconfig)
    dbconfig_dict = json.loads(dbconfig_str)  # 将字符串转成列表
    # print(dbconfig_dict)
    # print(type(dbconfig_dict))
    return dbconfig_dict



if __name__ == '__main__':
    # getZoneArray()
    # getemailUrl()
    # getzoneStatusUrl()
    getplatformAccessArray()