from django.shortcuts import render
import requests
from ast import literal_eval
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from utils import getfileProperty
import pymysql
import logging

"""运营管理"""


class EmailView(APIView):
    # 邮件视图
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        requestData = request.data
        zoneList = requestData.get('zoneList', '')  # 大区列表
        addressee = requestData.get('addressee', '')  # 收件人
        title = requestData.get('title', '')  # 标题
        content = requestData.get('content', '')  # 内容
        sendgoods = requestData.get('sendgoods', '')  # 赠送物品

        params_tuple = (zoneList, addressee, title, content)  # 判断必须参数
        if '' in params_tuple:
            return Response({'msg': '缺少必要参数', 'code': '400'})

        zoneList = literal_eval(zoneList)
        if 'gm' in addressee:
            addressee = addressee.split('gm')
        else:
            addressee = [addressee]

        email_dict_all = getfileProperty.getemailUrl()  # 获取到配置中邮件的路由
        email_list = []  # 初始化选择的需要发邮件的大区地址
        for k, v in email_dict_all.items():  # 遍历所有配置
            if k in zoneList:  # 如果配置中的键在传过来的大区列表里
                email_list.append(v)

        json_dict = {  # 封装json对象参数
            'cmd': 'send_mail',
            'admin': user.username,
            'title': title,  # 页面传入
            'content': content,  # 页面传入
            'chars': [0, 1, 2],  # 玩家角色id 的列表
            'items': [
                {'item_type': 1, 'item_count': 100},
                {'item_type': 2, 'item_count': 200}
            ]
        }


class SystemEmailView(APIView):
    # 系统邮件
    permission_classes = [IsAuthenticated]

    def post(self, request):
        requestData = request.data
        zoneList = requestData.get('zoneList', '')  # 大区列表
        addressee = requestData.get('addressee', '')  # 收件人
        title = requestData.get('title', '')  # 标题
        content = requestData.get('content', '')  # 内容
        gold = requestData.get('gold', '')  # 金币
        yuanbao = requestData.get('yuanbao', '')  # 元宝
        sendgoods = requestData.get('sendgoods', '')  # 赠送物品
        sendpet = requestData.get('sendpet', '')  # 赠送宠物
        arrivegrade = requestData.get('arrivegrade', '')  # 突破等级
        arrivestar = requestData.get('arrivestar', '')  # 升星等级
        flashlight = requestData.get('flashlight', '')  # 是否闪光
        petgrade = requestData.get('petgrade', '')  # 宠物等级
        personality = requestData.get('personality', '')  # 性格
        params_tuple = (zoneList, addressee, title, content)  # 判断必须参数
        if '' in params_tuple:
            return Response({'msg': '缺少必要参数', 'code': '400'})

        zonelist = literal_eval(zoneList)
        if 'gm' in addressee:
            addressee = addressee.split('gm')
        else:
            addressee = [addressee]


class HorseLampView(APIView):
    # 跑马灯
    permission_classes = [IsAuthenticated]

    def post(self, request):
        zoneList = request.data.get('zoneList', '')  # 大区列表
        time_start = request.data.get('time_start', '')
        time_end = request.data.get('time_end', '')
        interval_time = request.data.get('interval_time', '')
        content = request.data.get('content', '')
        if '' in (zoneList, interval_time, content):
            return Response({'msg': '缺少必要参数', 'code': '400'})

        zonelist = literal_eval(zoneList)


class GiftCodeView(APIView):
    # 礼包码
    permission_classes = [IsAuthenticated]
    pass


class ClientUpdateNoticeView(APIView):
    # 客户端更新通知
    permission_classes = [IsAuthenticated]

    def post(self, request):
        time_start = request.data.get('time_start', '')
        time_end = request.data.get('time_end', '')
