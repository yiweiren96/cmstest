from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from cmstest.utils.paginations import MyPageNumberPagination
from goods.models import Goods, GoodsCategory
from goods.serializers import RecommendSerializer, CategorySerializer, GoodsSerializer, DetailCategorySerializer


class RecommendGoodsView(ListAPIView):
    """推荐商品"""
    # goods/recommend/
    serializer_class = RecommendSerializer

    def get_queryset(self):

        return Goods.objects.filter(is_red=1).order_by('id')[:5]


class GoodsCategoryView(APIView):
    """商品目录"""
    # goods/category/

    def get(self, request):

        # 定义一个列表，存放返回数据
        goods_cat_lst = []

        # 获取一级目录对象列表
        bcats = GoodsCategory.objects.filter(parent=0)

        # 获取每个一级目录
        for bcat in bcats:
            bcat_data = CategorySerializer(bcat).data  # 字典类型

            # 查询该目录下的所有二级目录
            scats = bcat.goodscategory_set.all()  # set类型

            # 存放该目录下所有二级目录的id
            ids = []
            for scat in scats:
                ids.append(scat.id)

            # 获取该目录下所有二级目录的商品
            goods_query_set = Goods.objects.filter(category_id__in=ids)[:5]  # set

            goods = GoodsSerializer(goods_query_set, many=True).data  # set

            bcat_data['goods'] = goods

            goods_cat_lst.append(bcat_data)

        return Response(goods_cat_lst)


class GoodsListViewSet(ReadOnlyModelViewSet):
    """商品列表"""
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = MyPageNumberPagination
    filter_backends = [OrderingFilter]
    ordering_fields = ('create_time', 'sell_price', 'sales')

    def list(self, request, *args, **kwargs):
        # 获取查询参数
        cat_id = request.query_params['category']

        # 查询数据库，获取该目录
        try:
            cat = GoodsCategory.objects.get(id=cat_id)
        except GoodsCategory.DoesNotExist:
            return Response({'message': '该目录不存在'}, status=status.HTTP_400_BAD_REQUEST)

        # 判断是一级目录还是二级目录
        if cat.parent_id == 0:
            # 一级目录，返回该子目录所有的的商品
            scats = cat.goodscategory_set.all()

            # 统计所有子目录的id
            ids = []
            for scat in scats:
                ids.append(scat.id)

            # 查询商品数据库，将所属为该二级目录的商品选出来
            goods = Goods.objects.filter(category_id__in=ids)
            goods = self.filter_queryset(goods)
            page = self.paginate_queryset(goods)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = GoodsSerializer(goods, many=True)

            return Response(serializer.data)

        else:
            # 为二级目录，返回该目录下的所有商品
            goods = Goods.objects.filter(category_id=cat_id)
            goods = self.filter_queryset(goods)
            page = self.paginate_queryset(goods)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(goods, many=True)

            return Response(serializer.data)


class CategoryView(RetrieveAPIView):
    """商品分类"""
    queryset = GoodsCategory
    serializer_class = DetailCategorySerializer









