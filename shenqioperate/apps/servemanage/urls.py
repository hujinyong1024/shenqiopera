# -*- coding:utf-8 -*-
from django.urls import path
from . import views


urlpatterns = [
    path('servers/', views.ServerStatusView.as_view()),  # 区服管理获取及修改
]