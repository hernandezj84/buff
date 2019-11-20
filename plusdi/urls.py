from django.conf.urls import url
from plusdi import views

urlpatterns = [
    url('^plusdi/test/$', views.test),
    url('^plusdi/post-discount/$', views.post_discount),
    url('^plusdi/discount/$', views.get_discount),
    url('^plusdi/create-commerce/$', views.create_commerce),
    url('^plusdi/login-commerce/$', views.login_commerce),
    url('^plusdi/update-commerce/$', views.update_commerce)
]
