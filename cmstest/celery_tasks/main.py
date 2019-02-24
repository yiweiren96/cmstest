import os
from celery import Celery

# 设置setting文件
os.environ.setdefault('DJANGO_SETTINGS_MODULE','cmstest.settings.dev')

# 定义yigecelery应用(一个项目只需要一个celery应用)
# 参数１:自定义的应用名
# 参数2:耗时任务保存到redis
# 参数3:用老保存任务函数的执行结果
celery = Celery('cmstest',broker='redis://127.0.0.1:6379/15',backend='redis://127.0.0.1:6379/14')

# 从制定的包下,扫面任务函数
celery.autodiscover_tasks(['celery_tasks.sms','celery_tasks.email'])
