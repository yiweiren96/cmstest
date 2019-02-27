from rest_framework import serializers

from goods.models import Goods, GoodsCategory, GoodsAlbum


class RecommendSerializer(serializers.ModelSerializer):
    """商品推荐序列化器"""
    class Meta:
        model = Goods
        fields = ('id', 'title', 'img_url', 'update_time', 'create_time')


class SubCategorySerializer(serializers.ModelSerializer):
    """目录序列化器"""
    class Meta:
        model = GoodsCategory
        fields = ('id', 'title')


class CategorySerializer(serializers.ModelSerializer):
    """一级目录序列化器"""
    goodscategory_set = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = GoodsCategory
        fields = ('id', 'title', 'goodscategory_set')


class GoodsAlbumSerializer(serializers.ModelSerializer):
    """商品图片序列化器"""

    class Meta:
        model = GoodsAlbum
        fields = '__all__'


class DetailCategorySerializer(serializers.ModelSerializer):
    """"详情页商品目录序列化器"""
    parent = SubCategorySerializer()

    class Meta:
        model = GoodsCategory
        fields = ('id', 'title', 'parent')


class GoodsSerializer(serializers.ModelSerializer):
    """商品分类目录序列化器"""

    goodsalbum_set = GoodsAlbumSerializer(many=True, read_only=True)
    category = DetailCategorySerializer()

    class Meta:
        model = Goods
        fields = '__all__'
