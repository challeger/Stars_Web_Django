import datetime
import os
import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from shortuuidfield import ShortUUIDField


class Gender(models.TextChoices):
    MAN = '1', '男'
    WOMAN = '2', '女'
    SECRET = '3', '保密'


def _user_directory_path(instance, filename):
    now_date = datetime.datetime.now().strftime('%Y%m%d')  # 当天日期
    filename = '{}.{}'.format(uuid.uuid4().hex[:12], 'jpg')  # 随机生成文件名
    return os.path.join('user', 'avatar', now_date, filename)  # 返回生成的文件名


class UserManager(BaseUserManager):
    def _create_user(self, username, password, nickname, email, **kwargs):
        if not username:
            raise ValueError('请输入用户名!')
        if not password:
            raise ValueError('请输入密码!')
        if not nickname:
            raise ValueError('请输入昵称!')
        if not email:
            raise ValueError('请输入邮箱!')
        if self.model.objects.filter(username=username):
            raise ValueError('用户名已存在!')
        if self.model.objects.filter(nickname=nickname):
            raise ValueError('昵称已存在!')
        if self.model.objects.filter(email=email):
            raise ValueError('邮箱已存在!')
        user = self.model(username=username, password=password, nickname=nickname, email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username, password, nickname, email, **kwargs):
        kwargs['is_superuser'] = False
        return self._create_user(username, password, nickname, email, **kwargs)

    def create_superuser(self, username, password, nickname, email, **kwargs):
        kwargs['is_superuser'] = True
        return self._create_user(username, password, nickname, email, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    uid = ShortUUIDField(primary_key=True)  # 用户标识
    username = models.CharField(max_length=15, verbose_name='用户名', unique=True)
    email = models.EmailField('邮箱')
    avatar = models.ImageField(upload_to=_user_directory_path, blank=True,
                               default='user/avatar/default', verbose_name='头像')
    nickname = models.CharField(max_length=20, verbose_name='昵称', unique=True, db_index=True)
    gender = models.CharField(max_length=2, choices=Gender.choices, blank=True, default=Gender.SECRET)
    desc = models.CharField(max_length=50, blank=True, default='我们的征途是星辰大海!', verbose_name='个性签名')
    exp = models.PositiveIntegerField(default=0, verbose_name='经验值')
    stars = models.PositiveBigIntegerField(default=0, verbose_name='星币')
    mon_tickets = models.PositiveIntegerField(default=0, verbose_name='月票')
    re_tickets = models.PositiveIntegerField(default=0, verbose_name='推荐票')
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='注册时间')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ('nickname', 'email')
    EMAIL_FIELD = 'email'

    objects = UserManager()

    def get_full_name(self):
        return self.nickname

    def get_short_name(self):
        return self.nickname

    def __str__(self):
        return self.nickname

    class Meta:
        verbose_name = verbose_name_plural = '用户'
        db_table = 'model_user'


class EmailType(models.TextChoices):
    REGISTER = '1', '用户注册'
    PASSWORD = '2', '修改密码'


class EmailValid(models.Model):
    """
    邮箱验证类,保存 用户注册 与 修改密码时
    的验证码邮件信息
    """
    email_type = models.CharField(max_length=2, choices=EmailType.choices,
                                  default=EmailType.REGISTER, verbose_name='邮件类别')
    code = models.CharField(max_length=6, verbose_name='验证码')
    email_address = models.EmailField(verbose_name='邮箱地址')
    time = models.DateTimeField(auto_now_add=True, verbose_name='发送时间')

    class Meta:
        verbose_name = verbose_name_plural = '验证邮件'
        db_table = 'verify_email'
