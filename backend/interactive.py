#!/usr/bin/env python
#-*-coding:utf-8-*-

from web import models
from ZkFortress import settings
import getpass
import subprocess
import random
import string

from django.contrib.auth import authenticate
#django自带用户验证


class InteractiveHandler(object):
    #负责与用户在命令行端所有的交互
    def __init__(self,*args,**kwargs):
        '''
        from web import models
        print(models.Host.objects.all())
        自己写的不能直接调用数据库
        得先导入django例：main.py
        '''
        if self.authenticate():
            #authenticate认证如果成立执行interactive
            self.interactive()
    def authenticate(self):
        '''用户认证'''
        retry_count = 0 #密码重复次数
        while retry_count < 3:
            username = input("Username:").strip()
            #strip()去空格
            if len(username)==0:continue
            password = getpass.getpass("Password:")

            #在settings AUTH_USER_MODEL = 'web.UserProfile'声明用那张表
            #导入from django.contrib.auth import authenticate
            '''
            authenticate()： 认证给出的用户名和密码，使用 authenticate() 函数。
            它接受两个参数，用户名 username 和 密码 password ，并在密码对用
            给出的用户名是合法的情况下返回一个 User 对象。当给出的密码不合
            法的时候 authenticate() 函数返回 None
            '''
            user = authenticate(username=username,password=password)
            #print(user,type(user))
            #aa@123.com <class 'web.models.UserProfile'>

            if user is not None:#必须是这个格式djang自带
                print("\033欢迎登陆%s\033[0m".center(50,'-'),user)
                self.user = user
                #self.user是一个对向<class 'web.models.UserProfile'>
                return True
                #用户名密码匹配返回一个True调用interactive函数
            else:
                print("用户名或者密码不正确")
                retry_count += 1
        else:
            exit("超过三次")

    def create_session(self,bind_host_obj,random_tag):
        session_obj = models.SessionRecord(
            user = self.user,
            bind_host = bind_host_obj,
            rand_tag = random_tag
        )
        session_obj.save()#提交修改内容，可以直接获取id
        return session_obj


    def select_hosts(self,bind_host_list):
        '''
        处理用户选项
        '''
        #exit_flag=False

        while True:
            # bind_host_list = host_groups[user_choice].bind_hosts.select_related()
            for index,host_obj in enumerate(bind_host_list):
                print("%s \t%s" %(index,host_obj))
            user_choice2 = input("[%s]>>>" %self.user).strip()
            if user_choice2.isdigit():
                user_choice2 = int(user_choice2)
                if user_choice2 >=0 and user_choice2 < len(bind_host_list):
                    print('---host:',bind_host_list[user_choice2],type(bind_host_list[user_choice2]))
                    bind_host_obj = bind_host_list[user_choice2]
                    
                    random_tag = ''.join(random.sample(string.ascii_lowercase,14))
                    session_obj = self.create_session(bind_host_obj,random_tag)#创建一个会话记录
                    cmd_str = "sh %s %s %s"%(settings.SESSION_TRACK_SCRIPT,session_obj.id,session_obj.rand_tag)
                    print("tracking...",cmd_str)
                    session_track_obj=subprocess.Popen(cmd_str,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

                    cmd = "sshpass -p%s /usr/local/openssh7/bin/ssh %s@%s -p %s -o StrictHostKeyChecking=no -Z %s"%(
                                             bind_host_obj.remote_user.password,
                                             bind_host_obj.remote_user.username,
                                             bind_host_obj.host.ip_addr,
                                             bind_host_obj.host.port,
                                             random_tag)
                    print(
                        bind_host_obj,
                        bind_host_obj.remote_user.username,
                        bind_host_obj.host.ip_addr,
                        bind_host_obj.host.port)
                    subprocess.run(cmd,shell=True)
            else:
                if user_choice2 == "b" or user_choice2 == "B":
                    break
                if user_choice2 == 'exit' or user_choice2 == 'EXIT':
                    exit('bye')


    def interactive(self):
        '''用户shell'''

        exit_flag = False
        host_groups = self.user.host_groups.select_related()

        while not exit_flag:
            try:
                for index,group_obj in enumerate(host_groups):
                    #enumerate 函数用于遍历序列中的元素以及它们的下标
                    print("%s \t%s [%s]" %(index,
                                         group_obj,
                                         group_obj.bind_hosts.select_related().count()))
                                        #   select_related()列出与用户相关的bind_hosts
                print("z\t未分组主机列表[%s]" %self.user.bind_hosts.select_related().count())
                #显示未分组有多少台机器


                user_choice = input("[%s]>>>" %self.user).strip()
                #打印完让用户选择   self.user.strip()显示用户名
                if len(user_choice) == 0:continue
                if user_choice.isdigit():
                #is_digit如果字符串只包含数字则返回 True 否则返回 False
                    user_choice=int(user_choice)
                    if user_choice >= 0 and user_choice < len(host_groups):
                        self.select_hosts(host_groups[user_choice].bind_hosts.select_related())
                else:
                    if user_choice == 'z':
                        self.select_hosts(self.user.bind_hosts.select_related())
                    if  user_choice == 'exit':
                        exit('bye')
            except KeyboardInterrupt as e: #处理ctrl c
                pass





