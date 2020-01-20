from django.shortcuts import render
import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from utils import getfileProperty
import pymysql
import logging
from ast import literal_eval
from django.core.cache import cache, caches  # 由于渠道修改比较少，可以设置缓存


logger = logging.getLogger('django')


class ChannelStatusView(APIView):
    """渠道管理"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        response = cache.get('channelstatus')  # 尝试从缓存中获取数据

        if response is None:  # 如果缓存中没有数据就去数据库查询
            response = {'msg': '获取数据成功', 'code': '200', 'data': []}
            platform_list = getfileProperty.getplatformAccessArray()
            # 执行mysql查询语句获取到实际的值也加入到line_data里面
            dbconfig = getfileProperty.getdbconfig('pkmmaindb')  # 渠道管理只放在唯一主数据库中
            # 查询都是在同一个数据库中，可以将连接对象放在最外面
            conn = pymysql.Connect(**dbconfig)
            cursor = conn.cursor()
            for f_pf in platform_list:
                f_pf_t = f_pf['platform_type']
                f_pf_n = f_pf['platform_name']
                for childList in f_pf['childList']:
                    c_pf_t = childList['child_platform_type']
                    c_pf_n = childList['child_platform_name']
                    c_ID = childList['ID']
                    # 把每条子渠道的信息封装在字典里，并且添加到返回响应的data列表里
                    line_data = {
                        'platform_type': f_pf_t,
                        'platform_name': f_pf_n,
                        'child_platform_type': c_pf_t,
                        'child_platform_name': c_pf_n,
                        'ID': c_ID
                    }

                    # 查询可见区服，是否使用公告，编辑公告内容
                    sql1 = "SELECT access_servers, use_notice, notice_content FROM platform_access_server_info WHERE platform_type = %s AND child_platform_type = %s LIMIT 1;"
                    line = cursor.execute(sql1, [f_pf_t, c_pf_t])
                    if line != 0:
                        result = cursor.fetchone()
                        # district_service, use_notice, notice_content = result
                        district_service, use_notice, notice_content = result  # fetchon 获取到一个元祖可以直接赋值
                        # print(district_service)  # 获取到的字节需要解析，第一个字节是长度 后面是每2个字节代表一个大区号
                        # 数据库中是用小端法存储，把字节转成数字，先获取到长度
                        d_s_len = int.from_bytes(district_service[0:1], byteorder='little')
                        d_s_all = district_service[1:]  # 去掉表示长度的字节，剩下的就是大区信息
                        i = 0
                        line_data['district_service'] = []  # 为了是区号都能添加到列表，得一开始定义成空字符串
                        for j in range(d_s_len):
                            d_s = d_s_all[i: i+2]
                            d_s_n = int.from_bytes(d_s, byteorder='little')
                            line_data['district_service'].append(d_s_n)
                            i += 2
                        line_data['usr_notice'] = use_notice
                        line_data['notice_content'] = notice_content
                    # 查询是否可以充值语句
                    sql2 = "SELECT child_platform_type FROM platform_not_allow_recharage_info WHERE platform_type = %s AND child_platform_type = %s LIMIT 1;"
                    line = cursor.execute(sql2, [f_pf_t, c_pf_t])
                    if line == 0:  # 表里没有数据就表示允许充值
                        line_data['is_recharge'] = True
                    else:
                        line_data['is_recharge'] = False
                    response['data'].append(line_data)

            cursor.close()
            conn.close()

            cache.set('channelstatus', response, 24 * 1 * 60 * 60)  # 查询到的结果进行缓存

        return Response(response)

    def post(self, request):
        cache.delete('channelstatus')   # 有修改就清除缓存

        platformType = request.data.get('platformType', '')
        childPlatformType = request.data.get('childPlatformType', '')
        accessZones = request.data.get('accessZones', '')  # 包含数字大区号的列表
        allowRecharge = request.data.get('allowRecharge', 1)  # 固定为1
        useNotice = request.data.get('useNotice', 0)  # 固定为0
        noticContent = request.data.get('noticContent', '')  # 固定为空字符串
        if '' in (platformType, childPlatformType, accessZones):
            return Response({'msg': '缺少参数', 'code': '400'})
        accessZones = literal_eval(accessZones)  # 将列表字符串转换成列表
        paltformstatusurl = getfileProperty.getzoneStatusUrl()
        json_dict = {
            'cmd': 'platform_status',
            'platformType': int(platformType),
            'childPlatformType': str(childPlatformType),
            'accessZones': accessZones,
            'allowRecharge': int(allowRecharge),
            'useNotice': int(useNotice),
            'noticContent': noticContent
        }
        try:
            res = requests.post(url=paltformstatusurl, json=json_dict)  # 使用requests模块发起网络请求
        except Exception as e:
            logger.error('渠道修改失败')
            logger.error(e)
            return Response({'msg': '修改服务器错误', 'code': '500'})
        res_str = res.text
        print('res_str:', res_str)
        if res_str != 'success':
            return Response({'msg': '操作失败', 'code': '400'})
        else:
            response = {'msg': '操作成功', 'code': '200', 'data': []}
            line_data = {  # 要返回给前端的数据里的数据
                'platform_type': platformType,
                'child_platform_type': childPlatformType,
            }
            db_cfg = getfileProperty.getdbconfig('pkmmaindb')
            conn = pymysql.Connect(**db_cfg)
            cursor = conn.cursor()
            # 查询可见区服，是否使用公告，编辑公告内容
            sql1 = "SELECT access_servers, use_notice, notice_content FROM platform_access_server_info WHERE platform_type = %s AND child_platform_type = %s LIMIT 1;"
            line = cursor.execute(sql1, [platformType, childPlatformType])
            if line != 0:
                result = cursor.fetchone()
                # district_service, use_notice, notice_content = result
                district_service, use_notice, notice_content = result  # fetchon 获取到一个元祖可以直接赋值
                # print(district_service)  # 获取到的字节需要解析，第一个字节是长度 后面是每2个字节代表一个大区号
                # 数据库中是用小端法存储，把字节转成数字，先获取到长度
                d_s_len = int.from_bytes(district_service[0:1], byteorder='little')
                d_s_all = district_service[1:]  # 去掉表示长度的字节，剩下的就是大区信息
                i = 0
                line_data['district_service'] = []  # 为了是区号都能添加到列表，得一开始定义成空字符串
                for j in range(d_s_len):
                    d_s = d_s_all[i: i + 2]
                    d_s_n = int.from_bytes(d_s, byteorder='little')
                    line_data['district_service'].append(d_s_n)
                    i += 2
                line_data['usr_notice'] = use_notice
                line_data['notice_content'] = notice_content
            # 查询是否允许充值语句
            sql2 = "SELECT child_platform_type FROM platform_not_allow_recharage_info WHERE platform_type = %s AND child_platform_type = %s LIMIT 1;"
            line = cursor.execute(sql2, [platformType, childPlatformType])
            if line == 0:  # 表里没有数据就表示允许充值
                line_data['is_recharge'] = True
            else:
                line_data['is_recharge'] = False

            cursor.close()
            conn.close()

            response['data'].append(line_data)
            return Response(response)

