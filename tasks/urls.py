from django.conf.urls import url
from . import views
from django.contrib.auth.views import login, logout

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^search/$', views.search, name='search'),
    url(r'^task/addsubtasks$', views.addsubtask, name='addsubtask'),
    url(r'^task/(?P<id>.+)$', views.taskview, name='taskview'),
    url(r'^tasklist/(?P<id>.+)$', views.tasklistview, name='tasklistview'),

]
