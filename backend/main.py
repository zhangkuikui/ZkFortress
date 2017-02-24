#!/usr/bin/env python
#-*-coding:utf-8-*-
from backend import interactive

class ManagementUtily(object):
    def __init__(self,sys_args):
        #把zft_mgr.py的argv传进来
        '''分发用户命令'''
        self.sys_args = sys_args
        self.sys_verify()
        #验证传过来的参数，并调用用户指令对应的方法

    def show_help_msg(self):
        msg = '''
        run    启动堡垒机用户终端
        '''
        print(msg)

    def sys_verify(self):
        print(self.sys_args,len(self.sys_args))
        if len(self.sys_args) < 2:
            self.show_help_msg()
            #如果没有参数执行show_help_msg方法，返回运行脚本的方法
        elif hasattr(self,self.sys_args[1]):
            #判断有没有这个方法
            func = getattr(self,self.sys_args[1])
            #如果有用getattr + 括号执行这个方法
            func(self.sys_args)

        else:
            self.show_help_msg()
            #如果没有参数执行show_help_msg方法，返回运行脚本的方法

    def run(self,*args,**kwargs):
        '''启动用户交互程序'''

        # print("run...",'args:',args,'kwargs:',kwargs)
        interactive.InteractiveHandler(*args,**kwargs)
        '''
        调用interactive文件的Interactive类
        InteractiveHandler负责与用户在命令行端所有的交互
        *args,**kwargs（留出扩展）
        '''



