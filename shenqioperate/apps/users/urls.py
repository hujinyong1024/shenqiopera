# -*- coding:utf-8 -*-
from django.urls import path, include
from . import views


urlpatterns = [
    path('login/', views.LoginView.as_view()),
    path('test/', views.Test.as_view())
]