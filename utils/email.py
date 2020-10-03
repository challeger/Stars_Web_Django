#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""
@机构: 马士兵教育
@创建时间: 2020/9/30 17:45
@编写人: 小蓝同学
每天都要开心:)
"""
import time
from random import sample

from django.core.exceptions import ValidationError

from Users.models import EmailValid
from Stars_Web_Django.settings import EMAIL_EXP_DELTA


def get_random_code():
    # 随机返回一个6位的验证码
    chars = '1234567890poiuytrewqalskdjfhgnvmcxzbQWERTYUIOPLAKSJDHFGNBMVCXZ'
    return ''.join(sample(chars, 6))


def check_email(email, email_type, code):
    # 不存在则会抛出IndexError
    obj = EmailValid.objects.filter(email_address=email, email_type=email_type)[0]
    if obj.code != code:
        raise ValidationError('验证码错误!')
    email_time = time.mktime(obj.time.timetuple())
    if time.time() - email_time > EMAIL_EXP_DELTA:
        obj.delete()
        raise ValidationError('验证码已过期,请重新获取!')
    return obj
