from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token

from users import views
from users.views import AddressViewSet

urlpatterns = [
    # 检测用户名是否存在
    url(r'^usernames/(?P<username>\w{5,20})/count/$', views.UsernameCountView.as_view()),
    # 用户注册
    url(r'^users/$', views.CreateUserView.as_view()),

    url(r'^sms_codes/(?P<mobile>1[3-9]\d{9})/$', views.SmsCodeView.as_view()),

    # 登录obtain_jwt_token:登录视图(登录接口)
    url(r'^authorizations/$', obtain_jwt_token),

    # 获取所有的省份: /areas/
    url(r'^areas/$', views.AreaView.as_view()),
    # 获取城市或区县:  /areas/440100/
    url(r'^areas/(?P<pk>\d+)/$', views.SubAreaView.as_view()),

]

router = DefaultRouter()

router.register('addresses', AddressViewSet, base_name='address')
urlpatterns += router.urls
