


import optparse#参数处理
import sys,os


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ZkFortress.settings")
    import django
    django.setup()
    #先导入django
    from backend import main
    #再导入main函数

    main.ManagementUtily(sys.argv[0:])
    #如果没有默认是脚本的名字 sys.argv ['zft_mgr.py', 'run']

