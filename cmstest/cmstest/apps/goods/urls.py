from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from goods import views
from goods.views import GoodsListViewSet

urlpatterns = [
    url(r'^goods/recommend/$', views.RecommendGoodsView.as_view()),
    url(r'^goods/category/$', views.GoodsCategoryView.as_view()),
    url(r'^category/(?P<pk>\d+)/$', views.CategoryView.as_view()),

]


router = DefaultRouter()
router.register(r'goods', GoodsListViewSet, base_name='good')
urlpatterns += router.urls
