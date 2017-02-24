from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

#用于用户认证
from django.db.utils import IntegrityError
class IDC(models.Model):
    '''机房'''
    name = models.CharField(max_length=64,unique=True)
    #CharField()  字符型字段，默认的表单窗口部件是TextInput。该字段类型有一个必需参数：
    #max_length  在数据库水平限定了字符串最大长度
    #unique如果为True，则该字段必须是整个表中唯一的


    def __str__(self):
        return self.name
        #Python会调用对象的__str__方法，并输出那个方法所返回的字符串
        #返回自己


class Host(models.Model):
    hostname = models.CharField(max_length=64,unique=True)
    #主机名称
    ip_addr = models.GenericIPAddressField()
    #IPAddressField 一个IP地址，以字符串格式表示（例如： "24.124.1.30" ）。
    port = models.SmallIntegerField(default=22)
    #SmallIntegerField和IntegerField 类似，但是只允许在一个数据库相关的范围内的数值（通常是-32,768到+32,767）
    #default 字段的默认值

    idc =models.ForeignKey('IDC',blank=True,null=True)
    #ForeignKey 多对一
    #ManyToManyField 多对多
    #OneToOneField  一对一
    #blank 如果是 True ，该字段允许留空，默认为 False 。
    #如果设置为 True 的话，Django将在数据库中存储空值为 NULL 。默认为 False 。

    system_type_choices = ((0,'Linux'),(1,'Windows'))
    system_type = models.SmallIntegerField(choices=system_type_choices,default=0)
    memo = models.CharField(max_length=128,blank=True,null=True)
    #备注
    #choices 一个包含双元素元组的可迭代的对象，用于给字段提供选项。

    enabled = models.BooleanField(default=True,verbose_name="启用本机")
    def __str__(self):
        return "%s(%s)"%(self.hostname,self.ip_addr)
    #verbose_name数据可以通过queryset语句来获取

    class Meta:
        unique_together = ('ip_addr','port')
    def __str__(self):
        return "%s%s"%(self.hostname,self.ip_addr)
    #联合唯一


class RemoteUser(models.Model):
    '''存储远程用户信息'''
    auth_type_choices = ((0,'ssh-password'),(1,'ssh-key'))
    auth_type = models.SmallIntegerField(choices=auth_type_choices,default=0)
    username = models.CharField(max_length=128)
    password = models.CharField(max_length=256,help_text='如果auth_type选择为ssh-key，那此处就应该是key的路径')
    #在管理界面表单对象里显示在字段下面的额外帮助文本（可以不写）

    def __str__(self):
        return self.username
    class Meta:
        unique_together = ('auth_type','username','password')


class BindHost(models.Model):
    '''关联远程主机与远程用户'''
    host = models.ForeignKey('Host')
    remote_user = models.ForeignKey('RemoteUser')
    def __str__(self):
        return "<%s：%s>" %(self.host.hostname,self.remote_user.username)
    class Meta:
        unique_together = ('host','remote_user')




class HostGroups(models.Model):
    '''主机组，在主机组里面绑定能访问那些机器'''
    name = models.CharField(max_length=64,unique=True)
    bind_hosts = models.ManyToManyField('BindHost',blank=True)
    memo = models.CharField(max_length=128,blank=True,null=True)

    def __str__(self):
        return self.name




# from web import models as web_models
#ayth.py导入web.models重命名为web_models
class UserProfileManager(BaseUserManager):
    #表名更改MyUserManager改为UserProfileManager
    def create_user(self, email, name, password=None):
        #把传进来的参数date_of_birth改为name
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
            #首先确认有email
        user = self.model(
            email=self.normalize_email(email),
            #判断邮件地址是否合法
            name = name
            #创建用户
            #把date_of_birth=date_of_birth,name=name
        )

        user.set_password(password)
        #创建密码
        user.save(using=self._db)
        #把用户密码存到self._db，然后sava保存
        return user

    def create_superuser(self, email, name, password):
        #把传进来的参数date_of_birth改为name
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name = name
            #创建用户
            #把date_of_birth=date_of_birth,name=name
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser):
    #自己的表
    email = models.EmailField(
        #定义用户名是不是email
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    #date_of_birth = models.DateField()
    #出生日期
    name = models.CharField(max_length=32)
    #名字
    is_active = models.BooleanField(default=True)
    #是不是活跃
    is_admin = models.BooleanField(default=False)
    #是不是管理员
    bind_hosts = models.ManyToManyField('BindHost',blank=True)
    #关联远程主机与远程用户
    host_groups = models.ManyToManyField('HostGroups',blank=True)
    #关联那些组

    objects = UserProfileManager()
    #把MyUserManager改为UserProfileManager
    # 关联UserProfileManager
    #写死了的

    USERNAME_FIELD = 'email'
    #把那个字段当做用户名字段
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


    # class UserProfile(models.Model):
    #     '''堡垒机账户'''
    #     user = models.OneToOneField(User)
    #     name = models.CharField(max_length=32)

        # def __str__(self):
            # return  self.name


class SessionRecord(models.Model):
    '''记录ssh会话'''
    user = models.ForeignKey('UserProfile',verbose_name="堡垒机账户")
    bind_host = models.ForeignKey('BindHost')#关联的远程主机和账号
    rand_tag = models.CharField(max_length=64)#随机值
    date = models.DateTimeField(auto_now_add=True)#开始时间
    def __str__(self):
        return "<%s %s>"%(self.user.email,self.bind_host)
