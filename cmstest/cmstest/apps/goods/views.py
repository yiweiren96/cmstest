from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from cmstest.utils.paginations import MyPageNumberPagination
from goods.models import Goods
from goods.serializers import HotGoodsSerializer


class GooodsTestView(APIView):

    def get(self, request):
        return Response({'message': 'OK'})


class hot_goods(ListAPIView):
    pagination_class = MyPageNumberPagination
    serializer_class = HotGoodsSerializer

    def get_queryset(self):
        return Goods.objects.filter(is_red=1).order_by('id')
