from django.shortcuts import render
from django.views import View
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView


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