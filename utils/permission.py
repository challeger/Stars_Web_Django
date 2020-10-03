#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""
@机构: 马士兵教育
@创建时间: 2020/10/3 21:25
@编写人: 小蓝同学
每天都要开心:)
"""
from django.shortcuts import redirect
from django.urls import reverse

from Users.models import User


def check_login(func):
    def wrapper(request, *args, **kwargs):
        if isinstance(request.user, User):
            return func(request, *args, **kwargs)
        else:
            # 没有登录则重定向到登录页面
            return redirect(reverse('Users:login'))
    return wrapper
