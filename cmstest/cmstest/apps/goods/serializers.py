from rest_framework import serializers

from goods.models import Goods


class HotGoodsSerializer(serializers.ModelSerializer):
    # url(r'recommendations/$')
    class Meta:
        model = Goods
        fields = ('id', 'title', 'img_url', 'update_time', 'create_time')
