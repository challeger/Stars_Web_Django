import json

from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.db import DataError, IntegrityError
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import require_POST, require_GET

from Stars_Web_Django.settings import EMAIL_FROM
from Users.models import (
    User, EmailValid, EmailType,
    Gender, UserIdentity, Author
)
from utils.email import get_random_code, check_email
from utils.permission import check_login, is_not_author, is_identity, is_author


@require_POST
def login_auth(request):
    """
    登录认证
    :param request:
    :return:
    """
    try:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.get(Q(username=username) | Q(email=username))
        # 验证密码
        if not user.check_password(password):
            return JsonResponse(status=400, data={'status': 2, 'msg': '用户名或密码错误!'})
        obj = JsonResponse(data={'status': 1, 'msg': '登录成功!'})
        obj.set_cookie('Token', user.token, 60*60*24)
    # 未找到用户
    except User.DoesNotExist:
        return JsonResponse(status=400, data={'status': 2, 'msg': '用户名&邮箱未注册!'})
    return obj


@require_POST
def register(request):
    """
    注册接口
    :param request:
    :return:
    """
    try:
        username = request.POST.get('username')  # 用户名
        password = request.POST.get('password')  # 密码
        nickname = request.POST.get('nickname')  # 昵称
        email = request.POST.get('email')  # 邮箱
        check = request.POST.get('check')  # 验证码
        email_item = check_email(email, EmailType.REGISTER, check)
        User.objects.create_user(username, password, nickname, email)
        # 创建成功就删除对应的邮件
        email_item.delete()
    except ValueError as e:
        return JsonResponse(status=400, data={'status': 2, 'msg': str(e)})
    except ValidationError as e:
        return JsonResponse(status=400, data={'status': 2, 'msg': str(e)})
    return JsonResponse(data={'status': 1, 'msg': f'创建用户 {nickname} 成功'})


@require_POST
def email_register_verify(request):
    """
    注册时的发生验证码邮箱接口
    :param request:
    :return:
    """
    data = json.loads(request.body)
    resp = {}
    try:
        email = data['email']
        obj = User.objects.filter(email=email)
        if not obj:
            subject = '【群星小说网】欢迎加入群星小说网~请接收您的验证码'  # 邮件标题
            code = get_random_code()  # 获取一个随机的验证码
            text_content = f'我才不会告诉你验证码是 {code} 呢!'  # 邮件的文本格式
            html_content = f'<span>我才不会告诉你验证码是 <br><b>{code}</b><br> </span>呢!'  # 邮件的html格式
            msg = EmailMultiAlternatives(subject, text_content, EMAIL_FROM, [email])
            msg.attach_alternative(html_content, 'text/html')
            msg.send()
            resp['status'] = 1
            resp['msg'] = '发送邮件成功'
        else:
            resp['status'] = 2
            resp['msg'] = '邮箱已被注册!'
            return JsonResponse(status=400, data=resp)
    except Exception as e:
        # 简单的异常处理,后期需要进行细分.
        resp['status'] = 3
        resp['msg'] = str(e)
        return JsonResponse(status=400, data=resp)
    else:
        EmailValid.objects.create(code=code, email_address=email)
    # 成功就返回一个200状态码就行了.
    return JsonResponse(data=resp)


@require_GET
@check_login
def main(request):
    return render(request, 'users/center.html', context={'GENDER': Gender.choices})


@require_POST
@check_login
def modifyStars(request):
    """
    充值与消费星币接口
    :param request:
    :return:
    """
    data = json.loads(request.body)
    resp = {
        'status': 1,
        'msg': '',
    }
    try:
        count = int(data['count'])  # 获取要充值的数量
        request.user.stars += count  # 加上充值的金额
        request.user.save()  # 保存更改
        resp['msg'] = '充值成功!' if count > 0 else '消费成功!'
    except KeyError:
        resp['status'] = 2
        resp['msg'] = '不合法的参数!'
        return JsonResponse(status=400, data=resp)  # 这写法有点傻逼,后期优化下
    except DataError:
        resp['status'] = 2
        resp['msg'] = '余额不足,请充值!'
        return JsonResponse(status=400, data=resp)  # 这写法有点傻逼,后期优化下
    return JsonResponse(resp)


@require_POST
@check_login
def modifyUserInfo(request):
    """
    修改用户个人信息接口
    只能修改 昵称, 性别, 简介, 头像
    :param request:
    :return:
    """
    resp = {
        'status': 1,
        'msg': '',
    }
    try:
        nickname = request.POST.get('nickname')
        gender = request.POST.get('gender')
        desc = request.POST.get('desc')
        head_img = request.FILES.get('head-img')
        # 判断是否有空的数据
        if not all((nickname, gender)):
            raise DataError('数据不能为空!')

        user = request.user
        user.nickname = nickname
        user.gender = gender
        user.desc = desc

        if head_img:
            user.avatar = head_img

        user.save()
        resp['status'] = 1
        resp['msg'] = '修改信息成功'
    except KeyError:
        resp['status'] = 2
        resp['msg'] = '不合法的参数!'
        return JsonResponse(status=400, data=resp)  # 这写法有点傻逼,后期优化下
    except DataError as e:
        resp['status'] = 2
        resp['msg'] = str(e)
        return JsonResponse(status=400, data=resp)  # 这写法有点傻逼,后期优化下
    return JsonResponse(resp)


@require_POST
@check_login
def modifyPassword(request):
    """
    通过原密码来修改密码的接口
    :param request:
    :return:
    """
    resp = {
        'status': 1,
        'msg': '',
    }
    try:
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        if request.user.check_password(old_password):
            request.user.set_password(new_password)  # 修改密码
            request.user.save()  # 保存密码
            resp['msg'] = '修改密码成功!'
        else:
            resp['status'] = 2
            resp['msg'] = '原密码输入错误!'
    except Exception as e:
        print(e)
    return JsonResponse(resp)


@require_POST
@check_login
def email_modify_password_verify(request):
    """
    邮箱修改密码的发送验证码接口
    :param request:
    :return:
    """
    resp = {
        'status': 1,
        'msg': '',
    }
    try:
        subject = '【群星小说网】您正在尝试修改密码~'  # 邮件标题
        code = get_random_code()  # 获取一个随机的验证码
        text_content = f'我才不会告诉你验证码是 {code} 呢!'  # 邮件的文本格式
        html_content = f'<span>我才不会告诉你验证码是 <br><b>{code}</b><br> </span>呢!'  # 邮件的html格式
        msg = EmailMultiAlternatives(subject, text_content, EMAIL_FROM, [request.user.email])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()
        resp['status'] = 1
        resp['msg'] = '发送邮件成功'
    except Exception as e:
        print(e)
    else:
        EmailValid.objects.create(code=code, email_address=request.user.email, email_type=EmailType.PASSWORD)
    return JsonResponse(resp)


@require_POST
@check_login
def modify_password_with_email(request):
    """
    通过邮箱验证来修改密码的接口
    :param request: 请求
    :return:
    """
    resp = {
        'status': 1,
        'msg': ''
    }
    try:
        code = request.POST.get('code')
        email = check_email(request.user.email, EmailType.PASSWORD, code)  # 检查验证码
        password = request.POST.get('password')
        request.user.set_password(password)  # 修改密码
        request.user.save()  # 保存修改
        resp['msg'] = '修改密码成功'
        email.delete()  # 修改成功后删除对应邮件
    except Exception as e:
        resp['status'] = 2
        resp['msg'] = str(e)
    return JsonResponse(resp)


@require_POST
@check_login
def user_identity(request):
    """
    用户实名认证接口
    :param request:
    :return:
    """
    status = 200
    resp = {
        'status': 1,
        'msg': ''
    }
    try:
        name = request.POST.get('name')
        id_card = request.POST.get('id_card')
        if request.user.is_identity:
            resp['status'] = 2
            resp['msg'] = '已完成实名认证'
            status = 400
        else:
            UserIdentity.objects.create(user=request.user, name=name, id_card=id_card)
            resp['msg'] = '实名认证成功!'
    except Exception as e:
        resp['status'] = 2
        resp['msg'] = str(e)
        status = 400
    return JsonResponse(status=status, data=resp)


# 作者注册平台接口
@method_decorator((check_login, is_identity, is_not_author), name='dispatch')
class AuthorApplicationView(View):
    template_name = 'author/become_author.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        try:
            if name:
                Author.objects.create(user=request.user, author_name=name)
            else:
                return JsonResponse(status=400, data={'msg': '笔名不能为空!'})
        except IntegrityError:
            return JsonResponse(status=400, data={'msg': '笔名已被注册!'})
        return JsonResponse({'msg': 'ok'})


@check_login
@is_author
def author_index(request):
    return render(request, 'author/index.html')
