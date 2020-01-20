# -*- coding:utf-8 -*-
from django.urls import path, include
from . import views


urlpatterns = [
    path('channels/', views.ChannelStatusView.as_view())
]