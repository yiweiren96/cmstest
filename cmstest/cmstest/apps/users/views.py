from django.shortcuts import render
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView


class TestView(View):

    def get(self,request):
        return render(request,'test.html')


class TestView2(APIView):

    def get(self, request):
        # aa = 1 / 0
        return Response({'message': 'get请求'})

    def post(self, request):
        return Response({'message': 'post请求'})