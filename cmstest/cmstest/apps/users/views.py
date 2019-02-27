from django.shortcuts import render
from django.views import View
from rest_framework import mixins
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from django_redis import get_redis_connection
from redis.client import StrictRedis
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
import random

import logging

from rest_framework.viewsets import GenericViewSet
from rest_framework_extensions.cache.mixins import ListCacheResponseMixin, RetrieveCacheResponseMixin

from celery_tasks.sms.tasks import send_sms
from cmstest.libs.yuntongxun.sms import CCP
# /test/
from users.models import User, Area
from users.serializers import CreateUserSerializer, SubAreaSerializer, AreaSerializer, UserAddressSerializer


class UsernameCountView(APIView):
    """判断用户名是否重复"""

    def get(self, request, username):
        count = User.objects.filter(username=username).count()

        context = {
            'username': username,
            'count': count,
        }
        return Response(context)


class CreateUserView(CreateAPIView):
    """注册用户"""

    serializer_class = CreateUserSerializer
    print(serializer_class)


logger = logging.getLogger('django')


class SmsCodeView(APIView):
    def get(self, request, mobile):
        strict_redis = get_redis_connection('sms_codes')  # type:StrictRedis

        # 校验短信验证码是否重复发送(1分钟内禁止重复发送)
        send_flag = strict_redis.get('send_flag_%s' % mobile)
        if send_flag:
            raise ValidationError({'message': '频繁获取短信验证码'})

        # 生成短信验证码(云通讯)
        sms_code = '%06d' % random.randint(0, 999999)
        logger.info('短信验证码:%s %s' % (mobile.sms_code))

        # # 2. 发送短信验证码(云通讯)
        # CCP().send_template_sms(mobile, [sms_code, 5], 1)
        # sleep(5)
        # 使用celery来发送短信, 可以解决阻塞问题
        send_sms.delay('13600000000', '123456')

        # 使用管道优化代码
        pipeline = strict_redis.pipeline()
        pipeline.setex('sms_%s' % mobile, 60 * 5, sms_code)
        pipeline.setex('send_flag_%s' % mobile, 60, 1)
        result = pipeline.execute()  # 管道列表
        print(result)

        # 响应数据
        return Response({'message': 'OK'})


class AreaView(ListCacheResponseMixin, ListAPIView):
    """查询所有的省份"""

    queryset = Area.objects.filter(parent=None)
    # queryset = User.objects.filter(parent=None)
    serializer_class = AreaSerializer

    # 禁用分页功能
    pagination_class = None


# /areas/440100/
class SubAreaView(RetrieveCacheResponseMixin, RetrieveAPIView):
    """查询城市或区县(查询一条区域数据)"""

    queryset = Area.objects.all()
    serializer_class = SubAreaSerializer


class AddressViewSet(mixins.CreateModelMixin, GenericViewSet):
    """
    用户地址管理:6个接口
    1.地址增删改查(查多条) 4个
    2.设置默认地址:put
    3.设置地址标题:put
    """

    serializer_class = UserAddressSerializer
    permission_classes = [IsAuthenticated]  # 登录才能调用

    def get_queryset(self):
        # 返回当前登录用户所有的地址
        return self.request.user.addresses.filter(is_deleted=False)

    # 需求: 限制返回的地址个数
    def create(self, request, *args, **kwargs):
        count = request.user.addresses.count()
        if count >= 5:  # 每个用户最多不能超过5个地址
            return Response({'message': '地址个数已达到上限'}, status=400)

        return super().create(request, *args, **kwargs)

    # 重写list方法
    def list(self, request, *args, **kwargs):
        """ 用户地址列表数据 """
        queryset = self.get_queryset()  # 当前登录用户的所有地址
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'user_id': request.user.id,
            'default_address_id': request.user.default_address_id,
            'limit': 10,
            'addresses': serializer.data  # 列表
        })

    def status(self, request, pk=None):
        """
        设置默认地址
        :param request:
        :param pk:
        :return:
        """
        address = self.get_object()
        request.user.default_address = address
        request.user.save()
        return Response({'message': 'OK'},status=200)