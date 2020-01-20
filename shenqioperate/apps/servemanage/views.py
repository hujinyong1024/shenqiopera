from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from utils import getfileProperty
import pymysql
import requests
import logging

logger = logging.getLogger('django')

class ServerStatusView(APIView):
    """区服管理"""

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        response_content = {'msg': '获取数据成功', 'code': '200', 'data': []}
        zone_dict = getfileProperty.getZoneArray()
        for zoneID, zoneName in zone_dict.items():
            line_data = {'zoneID': zoneID, 'zoneName': zoneName}  # 需要返回的每一条内容
            db_cfg_v = 'pkm%s' % zoneID
            db_cfg = getfileProperty.getdbconfig(db_cfg_v)
            conn = pymysql.Connect(**db_cfg)
            cursor = conn.cursor()
            sql_zone_status = "SELECT zone_status FROM zone_status_info WHERE zone_id = %s LIMIT 1;"
            line_num = cursor.execute(sql_zone_status, [zoneID])
            if line_num == 0:
                line_data['error'] = '此数据库配置有误'
                response_content['data'].append(line_data)
                continue
            else:
                zoneStatus = cursor.fetchone()[0]
                line_data['zoneStatus'] = zoneStatus
            sql_maintenance = "SELECT zone_maintenance_status FROM zone_maintenance_info WHERE zone_id = %s LIMIT 1;"
            line_num = cursor.execute(sql_maintenance, [zoneID])
            if line_num == 0:
                line_data['error'] = '此数据库配置有误'
                response_content['data'].append(line_data)
                continue
            else:
                zoneMaintenanceStatus = cursor.fetchone()[0]
                line_data['zoneMaintenanceStatus'] = zoneMaintenanceStatus
            sql_recommend = "SELECT zone_recommend_status FROM zone_recommend_info WHERE zone_id = %s LIMIT 1;"
            line_num = cursor.execute(sql_recommend, [zoneID])
            if line_num == 0:
                line_data['error'] = '此数据库配置有误'
                response_content['data'].append(line_data)
                continue
            else:
                zoneRecommendStatus = cursor.fetchone()[0]
                line_data['zoneRecommendStatus'] = zoneRecommendStatus
            response_content['data'].append(line_data)
            cursor.close()
            conn.close()
        return Response(response_content)

    def post(self, request):
        zoneID = request.data.get('zoneID', '')
        zoneStatus = request.data.get('zoneStatus', '')
        zoneMaintenanceStatus = request.data.get('zoneMaintenanceStatus', '')
        zoneRecommendStatus = request.data.get('zoneRecommendStatus', '')
        if '' in (zoneID, zoneStatus, zoneMaintenanceStatus, zoneRecommendStatus):
            return Response({'msg': '缺少参数', 'code': '402'})
        zonestatusurl = getfileProperty.getzoneStatusUrl()
        json_dict = {  # 将参数封装成dict，requests模块能直接携带字典参数
            'cmd': 'server_status',  # 修改状态的表示
            'zoneID': int(zoneID),
            'zoneStatus': int(zoneStatus),
            'zoneMaintenanceStatus': int(zoneMaintenanceStatus),
            'zoneRecommendStatus': int(zoneRecommendStatus)
        }
        headers = {'Content-Type': 'application/json; charset=UTF-8'}
        try:
            res = requests.post(url=zonestatusurl, headers=headers, json=json_dict)  # 使用requests模块发起网络请求
        except Exception as e:
            logger.error('区服修改失败！')
            logger.error(e)
            return Response({'msg': '修改服务器错误', 'code': '500'})
        print(res)
        res_str = res.text
        print(res_str)
        if res_str != 'success':  # 返回响应不是success标明操作失败，直接返回信息
            return Response({'msg': '操作失败', 'code': '400'})
        else:  # 否则再去查询一遍数据库并返回修改后的信息
            response_content = {'msg': '操作成功', 'code': '200', 'data': []}
            line_data = {'dbnum': zoneID}  # 需要返回的每一条内容
            db_cfg_variable = 'pkm%s' % zoneID
            db_cfg = getfileProperty.getdbconfig(db_cfg_variable)
            conn = pymysql.Connect(**db_cfg)
            cursor = conn.cursor()
            sql_zone_status = "SELECT zone_status FROM zone_status_info WHERE zone_id = %s LIMIT 1;"
            cursor.execute(sql_zone_status, [zoneID])
            zoneStatus = cursor.fetchone()[0]
            line_data['zoneStatus'] = zoneStatus
            sql_maintenance = "SELECT zone_maintenance_status FROM zone_maintenance_info WHERE zone_id = %s LIMIT 1;"
            cursor.execute(sql_maintenance, [zoneID])
            zoneMaintenanceStatus = cursor.fetchone()[0]
            line_data['zoneMaintenanceStatus'] = zoneMaintenanceStatus
            sql_recommend = "SELECT zone_recommend_status FROM zone_recommend_info WHERE zone_id = %s LIMIT 1;"
            cursor.execute(sql_recommend, [zoneID])
            zoneRecommendStatus = cursor.fetchone()[0]
            line_data['zoneRecommendStatus'] = zoneRecommendStatus
            response_content['data'].append(line_data)
            return Response(response_content)


