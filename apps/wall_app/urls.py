from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^create$', views.create),
    url(r'^success$', views.success),
    url(r'^make_wish$', views.make_wish),
    url(r'^create_wish$', views.create_wish),
    url(r'^(?P<id>\d+)/del_wish$', views.del_wish),
    url(r'^(?P<id>\d+)/user_wishes$', views.user_wishes),
    url(r'^(?P<id>\d+)/remove_wishes$', views.remove_wishes),
    url(r'^(?P<item_name>\w+)/item_wishes$', views.item_wishes),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
]