"""shenqioperate URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', include('users.urls')),  # 管理员用户模块
    path('', include('usermanage.urls')),  # 用户管理模块
    path('', include('operatemanage.urls')),  # 运营管理模块
    path('', include('servemanage.urls')),  # 区服管理模块
    path('', include('channelmanage.urls'))  # 渠道管理模块

]
