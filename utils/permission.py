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


def is_identity(func):
    """
    判断用户是否已经通过认证
    """
    def wrapper(request, *args, **kwargs):
        if request.user.is_identity:
            return func(request, *args, **kwargs)
        else:
            return redirect(reverse('Users:center') + '#userIdentity')  # 跳转到认证页面
    return wrapper


def is_author(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_author:
            return func(request, *args, **kwargs)
        else:
            return redirect(reverse('Users:author_application'))
    return wrapper


def is_not_author(func):
    # 判断是否已经是作者了,是则跳到index页面,
    def wrapper(request, *args, **kwargs):
        if not request.user.is_author:
            return func(request, *args, **kwargs)
        else:
            return redirect(reverse('Users:author_index'))
    return wrapper
