#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""
@机构: 马士兵教育
@创建时间: 2020/10/3 17:00
@编写人: 小蓝同学
每天都要开心:)
"""
import time
from datetime import datetime

import jwt
from django.utils.deprecation import MiddlewareMixin

from Users.models import User
from Stars_Web_Django.settings import SECRET_KEY


class LoginMiddleware(MiddlewareMixin):
    def process_request(self, request):
        token = request.COOKIES.get('Token')
        if token:
            try:
                content = jwt.decode(token, key=SECRET_KEY)
                # 判断是否已经过期
                if time.time() < content['exp']:
                    request.user = User.objects.get(username=content['data']['username'])
            except KeyError:
                pass
            except jwt.exceptions.DecodeError:
                pass
            except User.DoesNotExist:
                pass
