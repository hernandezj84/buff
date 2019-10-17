from django.conf.urls import url
from api import views

urlpatterns = [
    url('^api/test/$', views.test),
    url('^api/workout/$', views.get_workout),
    url('^api/post-workout/$', views.post_workout)
]
