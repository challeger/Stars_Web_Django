#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""
@机构: 马士兵教育
@创建时间: 2020/9/30 14:39
@编写人: 小蓝同学
每天都要开心:)
"""
from django.urls import path, include
from django.views.generic import TemplateView

from Users import views

app_name = 'Users'

urlpatterns = [
    path('login/', TemplateView.as_view(template_name='users/login.html'), name='login'),
    path('login_auth/', views.login_auth, name='login_auth'),
    path('register/', views.register, name='register'),
    path('email_register_verify/', views.email_register_verify, name='email_register_verify'),
    path('email_modify_password_verify/', views.email_modify_password_verify, name='email_modify_password_verify'),
    path('center/', views.main, name='center'),
    path('modify_stars/', views.modifyStars, name='modify_stars'),
    path('modify_userInfo/', views.modifyUserInfo, name='modify_userInfo'),
    path('modify_password/', views.modifyPassword, name='modify_password'),
    path('modify_password_with_email/', views.modify_password_with_email, name='modify_password_with_email')
]
