from django.conf.urls import url
from goods import views

urlpatterns = [
    url(r'^goodstest/$', views.GooodsTestView.as_view()),
    url(r'^hotgoods/$', views.hot_goods.as_view()),
]
