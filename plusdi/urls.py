from django.conf.urls import url
from plusdi import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    url('^plusdi/test/$', views.test),
    url('^plusdi/post-discount/$', views.post_discount),
    url('^plusdi/discount/$', views.get_discount),
    url('^plusdi/create-commerce/$', views.create_commerce),
    url('^plusdi/login-commerce/$', views.login_commerce),
    url('^plusdi/login-user/$', views.login_user),
    url('^plusdi/update-commerce/$', views.update_commerce),
    url('^plusdi/get-commerce/$', views.get_commerce),
    url('^plusdi/get-discounts/$', views.get_commerce_discount),
    url('^plusdi/update-discount/$', views.update_commerce_discount),
    url('^plusdi/create-client', views.create_client),
    url('^plusdi/update-client-categories', views.update_client_categories),
    url('^plusdi/get-client-discounts', views.get_client_discounts),
    url('^plusdi/get-valid-discounts', views.get_commerce_valid_discount),
    url('^plusdi/get-client-match-documents', views.get_client_match_document),
    url('^plusdi/post-match-document', views.post_match_discount),
    url('^plusdiweb/*', views.backend),
]

urlpatterns += staticfiles_urlpatterns()
