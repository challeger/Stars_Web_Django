import json

from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.decorators.http import require_POST

from Stars_Web_Django.settings import EMAIL_FROM
from Users.models import User, EmailValid
from utils.data import post2dict, get_random_code


@require_POST
def login_auth(request):
    data = json.loads(request.body)
    try:
        user = User.objects.get(Q(username=data['username']) | Q(email=data['username']))
    except User.DoesNotExist:
        return
    except KeyError:
        pass
    return redirect(reverse('Users:login'))


@require_POST
def register(request):
    data = json.loads(request.body)
    print(data)
    try:
        username = data['username']  # 用户名
        password = data['password']  # 密码
        email = data['email']  # 邮箱
        check = data['check']  # 验证码
        if not all((username, password, email, check)):
            raise KeyError
    except KeyError:
        return JsonResponse(status=400, data={'status': 1, 'msg': '不合法的请求数据'})
    return redirect(reverse('Users:login'))


@require_POST
def email_register_verify(request):
    data = json.loads(request.body)
    # try:
    email = data['email']
    obj = User.objects.filter(email=email)
    if not obj:
        subject = '【群星小说网】欢迎加入群星小说网~请接收您的验证码'  # 邮件标题
        code = get_random_code()  # 获取一个随机的验证码
        print(code)
        text_content = f'我才不会告诉你验证码是 {code} 呢!'  # 邮件的文本格式
        html_content = f'<span>我才不会告诉你验证码是 <br><b>{code}</b><br> </span>呢!'  # 邮件的html格式
        msg = EmailMultiAlternatives(subject, text_content, EMAIL_FROM, [email])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()
    else:
        return JsonResponse(status=400, data={'status': 2, 'msg': '邮箱已被注册!'})
    # except Exception as e:
    #     # 简单的异常处理,后期需要进行细分.
    #     return JsonResponse(status=400, data={'status': 3, 'msg': str(e)})
    # else:
    #     EmailValid.objects.create(code=code, email_address=email)
    # 成功就返回一个200状态码就行了.
    return JsonResponse(None)
