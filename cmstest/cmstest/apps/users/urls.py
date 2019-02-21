from django.conf.urls import url
from users import views

urlpatterns = [
    url(r'^test/$',views.TestView.as_view()),
    url(r'^test2/$',views.TestView2.as_view()),
]
