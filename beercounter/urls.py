from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.front_list, name='list'),
    url(r'^user/([0-9]+)', views.user_detail, name="user_detail"),
    url(r'^up$', views.up, name='up'),
    url(r'^down$', views.down, name='down'),
    url(r'^remove_consumption/([0-9]+)$', views.remove_consumption, name='remove_consumption'),
    url(r'^stats$', views.last_drinks, name='stats'),
]
