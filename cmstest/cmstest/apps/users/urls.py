from django.conf.urls import url
from users import views

urlpatterns = [
    url(r'^test/$',views.TestView.as_view()),
    url(r'^test2/$',views.TestView2.as_view()),

    # 检测用户名是否存在
    url(r'^usernames/(?P<username>\w{5,20})/count/$', views.UsernameCountView.as_view()),
    # 用户注册
    url(r'^users/$', views.CreateUserView.as_view()),
    url(r'^sms_codes/(?P<mobile>1[3-9]\d{9})/$', views.SmsCodeView.as_view()),

]
