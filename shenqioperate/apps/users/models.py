from django.db import models
from django.contrib.auth.models import AbstractUser


class Admin(AbstractUser):
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')

    class Meta:
        db_table = 'admin'
        verbose_name = '管理员信息表'
        verbose_name_plural = verbose_name


class Admin_Login(models.Model):
    username = models.CharField(max_length=10, verbose_name='用户名')
    login_ip = models.CharField(max_length=16, verbose_name='登录ip')
    login_time = models.DateTimeField(auto_now_add=True, verbose_name='登录时间')

    class Meta:
        db_table = 'login_log'
        verbose_name = '登录日志'
        verbose_name_plural = verbose_name

