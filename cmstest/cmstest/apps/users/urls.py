from django.conf.urls import url
from users import views

urlpatterns = [
    url(r'^test/$',views.TestView.as_view()),
]
