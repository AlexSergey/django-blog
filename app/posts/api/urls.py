from django.conf.urls import url
from django.contrib import admin

# we can import all views methods only local app!
from .views import (
    PostDetailAPIView,
    PostListAPIView,
    PostUpdateAPIView,
    PostDeleteAPIView,
    PostCreateAPIView
)

# Post CRUD urls:
urlpatterns = [
    url(r'^$',                  PostListAPIView.as_view(),   name='list'),
    url(r'^create/$',           PostCreateAPIView.as_view(),   name='create'),
    url(r'^(?P<slug>[\w-]+)/$', PostDetailAPIView.as_view(), name='detail'),
    url(r'^(?P<slug>[\w-]+)/edit/$', PostUpdateAPIView.as_view(), name='update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', PostDeleteAPIView.as_view(), name='delete'),
]