from django.shortcuts import render
from django.views import View
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView


from django_redis import get_redis_connection
from redis.client import StrictRedis
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
import random

import logging

from celery_tasks.sms.tasks import send_sms
from cmstest.libs.yuntongxun.sms import CCP
# /test/
from users.models import User
from users.serializers import CreateUserSerializer

class TestView(View):

    def get(self,request):
        return render(request,'test.html')


class TestView2(APIView):

    def get(self, request):
        # aa = 1 / 0
        return Response({'message': 'get请求'})

    def post(self, request):
        return Response({'message': 'post请求'})

class UsernameCountView(APIView):
    """判断用户名是否重复"""

    def get(self,request,username):
        count = User.objects.filter(username=username).count()

        context = {
            'username':username,
            'count':count,
        }
        return Response(context)

class CreateUserView(CreateAPIView):
    """注册用户"""

    serializer_class = CreateUserSerializer
    print(serializer_class)



logger = logging.getLogger('django')

class SmsCodeView(APIView):

    def get(self,request,mobile):
        strict_redis = get_redis_connection('sms_codes')  # type:StrictRedis

        # 校验短信验证码是否重复发送(1分钟内禁止重复发送)
        send_flag = strict_redis.get('send_flag_%s' % mobile)
        if send_flag:
            raise ValidationError({'message':'频繁获取短信验证码'})

        # 生成短信验证码(云通讯)
        sms_code = '%06d' % random.randint(0,999999)
        logger.info('短信验证码:%s %s' % (mobile.sms_code))

        # # 2. 发送短信验证码(云通讯)
        # CCP().send_template_sms(mobile, [sms_code, 5], 1)
        # sleep(5)
        # 使用celery来发送短信, 可以解决阻塞问题
        send_sms.delay('13600000000', '123456')

        # 使用管道优化代码
        pipeline = strict_redis.pipeline()
        pipeline.setex('sms_%s' % mobile,60*5,sms_code)
        pipeline.setex('send_flag_%s' % mobile,60,1)
        result = pipeline.execute()  # 管道列表
        print(result)

        # 响应数据
        return Response({'message':'OK'})