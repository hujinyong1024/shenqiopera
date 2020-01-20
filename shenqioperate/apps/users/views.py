import datetime
from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Admin, Admin_Login
from django.core.cache import cache
import pymysql
import hashlib
from django.db import connection


class LoginView(APIView):
    authentication_classes = []  # 避免调用登录接口携带过期Token,此处要设置为空

    def post(self, request):
        if request.META.get('HTTP_X_FORWARDED_FOR'):
            login_ip = request.META.get("HTTP_X_FORWARDED_FOR")
        else:
            login_ip = request.META.get("REMOTE_ADDR")
        login_time = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        username = request.data.get('username', '').strip()
        password = request.data.get('password', '').strip()
        if username == '' or password == '':
            return Response({'msg': '缺少参数', 'code': '400'})


        ### django自带的认证，此项目中由于使用多个数据库和表新开服新部署较多，因此改写自带表的认证方式  ###
        # user = auth.authenticate(username=username, password=password)
        # if user and user.is_active:  # 登录成功
        #     del_token = Token.objects.filter(user=user).first()
        #     if del_token is not None:
        #         del_token.delete()
        #     auth.login(request, user)  # 实际是写入一条session到表中，增加cookie和session，激活用户的属性
                    # logout(request)  # 上一行的相对用法，清除cookie和session
        #     token, creatfalg = Token.objects.get_or_create(user=user)

        # 创建数据库连接对象
        # conn = pymysql.Connection(host=dbconfig.maindb['host'], port=3306, user=dbconfig.maindb['user'],
        #                      password=dbconfig.maindb['passwd'], database=dbconfig.maindb['dbname'], charset='utf8')
        # cursor = conn.cursor()
        # sql0 = "SELECT password FROM admin WHERE username = %s LIMIT 1;"
        # cursor.execute(sql0, [username])
        # result = cursor.fetchone()
        # realpwd = result[0]

        try:
            user = Admin.objects.get(username=username)
        except Admin.DoesNotExist:
            return Response({'msg': '用户名或密码错误', 'code': '401'})
        print(user)
        pwd = hashlib.md5(password.encode()).hexdigest()
        if pwd == user.password:
            del_token = Token.objects.filter(user=user).first()  # 查出对应的token
            if del_token is not None:  # 如果存在就删除之前的token，后面再写入新的token，更加安全
                del_token.delete()
            # auth.login(request, user)  # 这一步是干嘛的？ 写入一条django_session记录
            token, creatfalg = Token.objects.get_or_create(user=user)
            print(token)

            token_cache = 'Token_' + token.key  # 设置存入缓存中的键的名字，须和自定义验证里相同（未确认是否有效）
            cache.set(token_cache, token, 24 * 1 * 60 * 60)  # 添加 token_xxx 到缓存  1天有限期

            cursor = connection.cursor()
            sql1 = "SELECT login_ip, login_time FROM login_log ORDER BY id DESC LIMIT 1;"  # 查询出上一次登录地址和时间
            cursor.execute(sql1)
            result = cursor.fetchone()
            if result:
                last_ip = result[0]
                last_time = result[1]
            else:
                last_ip = '无'
                last_time = '无'
            print('last_time: ', last_time)
            sql2 = "INSERT INTO `login_log` VALUES (0, %s, %s, %s);"  # 将此次登录信息保存记录
            cursor.execute(sql2, [username, login_ip, login_time])
            cursor.close()
            responst_data = {
                'last_ip': last_ip,
                'last_time': last_time,
                'login_ip': login_ip,
                'login_time': login_time
            }
            ret = {'msg': '登录成功', 'code': '0', 'data': responst_data}
            return Response(ret, headers={'Token': token.key})
        else:
            ret = {'msg': '用户名或密码错误', 'code': '401'}
            return Response(ret)


class Test(APIView):
    permission_classes = [IsAuthenticated]
    # authentication_classes = (ExpiringTokenAuthentication, SessionAuthentication) # 配置到了settings里就不需要再设置

    def post(self, request):
        return Response({'msg': 'test'})

    def get(self, request):
        return Response({'msg': 'get test'})


