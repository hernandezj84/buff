from django.conf.urls import url
from plusdi import views

urlpatterns = [
    url('^plusdi/test/$', views.test),
    url('^plusdi/post-discount/$', views.post_discount),
    url('^plusdi/discount/$', views.get_discount),
    url('^plusdi/create-commerce/$', views.create_commerce),
    url('^plusdi/login-commerce/$', views.login_commerce),
    url('^plusdi/update-commerce/$', views.update_commerce),
    url('^plusdi/get-commerce/$', views.get_commerce),
    url('^plusdi/get-discounts/$', views.get_commerce_discount),
    url('^plusdi/update-discount/$', views.update_commerce_discount),
    url('^plusdi/create-client', views.create_client),
    url('^plusdi/update-client-categories', views.update_client_categories)
]
