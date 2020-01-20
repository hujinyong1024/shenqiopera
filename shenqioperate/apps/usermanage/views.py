from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import pymysql


class QueryUserInfoView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        query_type = request.data.get('query_type', '')
        account = request.data.get('account', '')
        uname = request.data.get('uname', '')
        if '' in (query_type, account) or '' in (query_type, uname):
            return Response({'msg': '缺少必要参数', 'code': '400'})
        if query_type == 'account':
            query_data = account
        elif query_type == 'uname':
            query_data = uname
        else:
            return Response({'msg': '查询类型不合理', 'code': '405'})


