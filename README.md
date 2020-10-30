# 群星小说网

## **项目说明**

**开发环境: python3.8 + django3.1**

**依赖:**

- **django**  # 开发框架
- **django-cors-headers**  # 解决跨域问题
- **mysql, mysqlclient**  # 连接mysql数据库
- **django-shortuuidfield**  # 自动生成用户的uid
- **PyJWT**  # 用于生成登录的token

本项目将会采用两种开发方式,分别是

- 前后端结合,即前后端都用django来做.
- 前后端分离,后端用drf来做,前端用vue来做.

**当前项目采用前后端结合实现**

**前后端分离项目地址:** 

后端: https://github.com/challeger/Starts_Web

前端: 暂无

本项目目标是实现一个大型的小说网站,目标功能包括 **用户的注册登录等基本操作(用邮箱验证实现)**, **用户的VIP等级**, **用户与作者两种身份**, **小说的订阅,投票等**

## **开发日志**

### **2020.09.30**

​	项目初始化,环境配置

​	创建Users模型,在settings.py中对 会用的到应用与数据库进行了配置

### **2020.10.02**

​	前端页面 登录注册页面的完成,表单数据的提交试用ajax来实现.

​	后台的邮箱验证逻辑还没实现,预计明天完成.

### **2020.10.03**

​	完成了邮箱注册功能.登录验证准备用jwt来做

​	使用中间件+jwt实现了登录验证,在用户登录后会设置一个 时长一天的 Token 在cookie上,然后通过中间件在每次请求中判断是否带有token,有则将request.user设置为获取到的user.

​	然后自定义一个验证装饰器,判断request.user是否是User类,是的话说明已经登录的.

### **2020.10.06**

​	完成了个人中心的前端页面

​	完成了充值星币与消费星币的功能(伪),后期要将充值接口接入支付宝和微信支付

### **2020.10.07**

​	用cropper做了上传头像的模态框

### **2020.10.08**

​	完成了头像上传.将个性签名改为可以为空

​	完成了修改密码(原密码修改与邮箱验证修改)

​	集成了message插件进行提示

### **2020.10.09**

​	1.解决了登录后的ajax重定向问题

​	2.新建User的两个一对一表, 分别是

​		**UserIdentity表** 用于存储用户的实名认证信息

​		**Author表** 用于存储用户的作者身份数据,每个用户都可以申请成为作者,前提是完成了实名认证

​		今天目标将 **实名认证** 与 **申请成为作者** 两个功能完成

​	3.完成了实名认证接口.

​		当使用一对一关系时,获取对应的值,如果不存在,那么抛出的异常类型是`DoesNotExist`,例如

​		这里判断用户是否进行了实名认证,就捕获`UserIdentity.DoesNotExist`异常

### **2020.10.10**

​	完成了作者申请功能

### **2020.10.12**

​	今天有点忙,就不搞了,不过基本确定作者后台用一个后台管理系统来改

### **2020.10.30**

​	时隔两周,终于有空稍微改了一下网上找的一个后台模板...把base模板弄了出来

## Bug记录

### **2020 09 30**

#### **1.自定义用户模型替换之后,创建迁移失败**

**原因:** 修改用户模型之前进行了迁移,数据库之前已经创建了与用户相关的依赖表

**修改:** 删库重建.

### **2020 10 02**

#### **1. CSRF验证**

**原因:** 在使用ajax提交表单数据时遇到了csrf验证问题

**解决办法:** 将ajax请求的请求头加上一个csrf token

```
$.ajaxSetup({
        beforeSend: function(xhr, settings){
            xhr.setRequestHeader("X-CSRFToken", "{{ csrf_token }}")
        }
    });
```

#### **2. SMTP出现编码问题**

**原因:** 计算机名中带了中文,导致出现**UnicodeDecodeError**

**解决办法:** 修改计算机名... (我是nt)

### **2020 10 03**

#### **1. 邮箱验证失败**

**原因:** 邮箱的验证密码失效

**解决办法:** 重新获取验证密码

### **2020 10 07**

#### **1. ajax请求无法重定向**

**原因:** 用ajax发送请求,无法处理后端的重定向响应.

**解决办法:** 如果把后端返回的重定向请求改为json数据类型可以处理,但我发现越写越像前后端分离的项目的..这个bug暂时放在一边

**2020 10 09 解决:** 让后端只传一个成功的响应回来,然后ajax的success回调进行重定向..感觉有点像前后端分离的写法=.=

### **2. cropper**

**原因:** cropper的裁剪框高度一直固定在100,影响正常使用.