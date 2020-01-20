# -*- coding:utf-8 -*-
"""   自定义校验模块，给接口提供状态保持    """
# import pytz
import pytz
from rest_framework.authentication import SessionAuthentication
from django.utils.translation import ugettext_lazy as _
from django.core.cache import cache
import datetime
from django.utils.six import text_type
from rest_framework.authentication import BaseAuthentication, TokenAuthentication
from rest_framework import exceptions
from rest_framework.authtoken.models import Token
from rest_framework import HTTP_HEADER_ENCODING


# 获取请求头里的token信息
def get_authorization_header(request):
    """
    Return request's 'Authorization:' header, as a bytestring.
    返回请求的“Authorization:”头，作为bytestring。

    Hide some test client ickyness where the header can be unicode.
    隐藏一些测试客户端ickyness，其中的头可以是unicode。
    """
    auth = request.META.get('HTTP_AUTHORIZATION', b'')  # 只能是这么获取到Authorization
    # print('获取到的HTTP_AUTHORIZATION： ', auth)

    if isinstance(auth, text_type):
        # Work around django test client oddness
        auth = auth.encode(HTTP_HEADER_ENCODING)
    return auth


# 自定义的ExpiringTokenAuthentication认证方式
class ExpiringTokenAuthentication(BaseAuthentication):
    model = Token

    def authenticate(self, request):
        auth = get_authorization_header(request)

        if not auth:
            return None
        try:
            token = auth.decode()
        except UnicodeError:
            msg = _('Invalid token header. Token string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)
        return self.authenticate_credentials(token)

    def authenticate_credentials(self, key):
        # 增加了缓存机制
        # 首先先从缓存中查找
        token_cache = key.replace(' ', '_')
        cache_user = cache.get(token_cache)
        try:
            if cache_user:
                # 更新缓存  更新 Token表
                token = self.model.objects.get(key=token_cache[6:])
                # token.created = datetime.datetime.now()
                # token.save()
                # cache.set(token_cache, token, 24 * 1 * 60 * 60)  # 参数为（键，值， 过期时间）

                today_now = datetime.datetime.today()
                token_created = token.created
                aa = today_now - token_created
                cc = aa.days
                if cc >= 1:
                    raise exceptions.AuthenticationFailed('认证信息过期请重新登录')

                return (cache_user.user, cache_user)  # 首先查看token是否在缓存中，若存在，返回用户

            token = self.model.objects.get(key=token_cache[6:])
            # token.created = datetime.datetime.now()
            # token.save()

        except self.model.DoesNotExist:
            raise exceptions.AuthenticationFailed('认证失败')

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed('用户被禁止')

        # utc_now = datetime.datetime.utcnow()
        # print('utc_now:', utc_now)
        # utc_s = utc_now.replace(tzinfo=pytz.timezone("UTC"))
        # print(utc_now.replace(tzinfo=pytz.timezone("UTC")))
        # utc_d = token.created.replace(
        #         tzinfo=pytz.timezone("UTC"))
        # hejiday = (utc_s - utc_d).days
        # print('hejiday:', hejiday)
        # if hejiday > 1:  # 设定存活时间 1天
        #     raise exceptions.AuthenticationFailed('认证信息过期请重新登录')

        today_now = datetime.datetime.today()
        token_created = token.created
        aa = today_now - token_created
        cc = aa.days
        if cc >= 1:
            raise exceptions.AuthenticationFailed('认证信息过期请重新登录')

        # todo 貌似用不到
        # if token:
        #     token_cache = key.replace(' ', '_')
        #     cache.set(token_cache, token, 24 * 1 * 60 * 60)  # 添加 token_xxx 到缓存  1天有限期
        return (token.user, token)

    def authenticate_header(self, request):
        return 'Token'
