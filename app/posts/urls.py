from django.conf.urls import url
from django.contrib import admin

# we can import all views methods only local app!
from .views import (
    posts_list,
    posts_create,
    posts_detail,
    posts_update,
    posts_delete
)

# Post CRUD urls:
urlpatterns = [
    url(r'^$',        posts_list, name='list'),
    url(r'^create/$', posts_create),
    url(r'^(?P<slug>[\w-]+)/$', posts_detail, name='detail'), # name - for link name
    url(r'^(?P<slug>[\w-]+)/edit/$', posts_update, name='update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', posts_delete),
]