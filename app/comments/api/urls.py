from django.conf.urls import url
from django.contrib import admin

# we can import all views methods only local app!
from .views import (
    CommentListAPIView,
    CommentDetailAPIView,
    CommentCreateAPIView,
    CommentEditAPIView
)

# Post CRUD urls:
urlpatterns = [
    url(r'^$',                  CommentListAPIView.as_view(),   name='list'),
    url(r'^create/$',      CommentCreateAPIView.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/$',      CommentDetailAPIView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/edit/$',      CommentEditAPIView.as_view(), name='edit'),
    #url(r'^(?P<id>\d+)/delete/$', PostDetailAPIView.as_view(), name='detail'),
]