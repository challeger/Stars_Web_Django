#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""
@机构: 马士兵教育
@创建时间: 2020/9/30 17:45
@编写人: 小蓝同学
每天都要开心:)
"""
from random import sample


def post2dict(content):
    # 根据request的body,获取上传的数据
    content = content.decode('utf-8').split('&')  # 拿到post数据的列表
    resp = {}
    for item in content:
        key, value = item.split('=')
        resp[key] = value
    return resp


def get_random_code():
    # 随机返回一个6位的验证码
    chars = '1234567890poiuytrewqalskdjfhgnvmcxzbQWERTYUIOPLAKSJDHFGNBMVCXZ'
    return ''.join(sample(chars, 6))
