from django.conf.urls import url
from django.contrib import admin

# we can import all views methods only local app!
from .views import (
    UserCreateAPIView,
    UserLoginAPIView
)

# Post CRUD urls:
urlpatterns = [
    url(r'^login/$', UserLoginAPIView.as_view(),   name='register'),
    url(r'^register/$', UserCreateAPIView.as_view(),   name='login')
]