from time import sleep

from celery_tasks.main import celery

@celery.task(name='send_sms')
def send_sms(mobile,sms_code):
    """获取短信验证码"""
    print("获取短信验证码: %s" % (sms_code))
    sleep(5)
    return sms_code