from django.conf.urls import url
from api import views

urlpatterns = [
    url('^plusdi/test/$', views.test),
]
