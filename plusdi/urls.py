from django.conf.urls import url
from api import views

urlpatterns = [
    url('^plusdi/test/$', views.test),
    url('^plusdi/post-discount/$', views.post_workout),
    url('^plusdi/discount/$', views.get_workout),
]
