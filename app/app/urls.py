"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from users.views import (login_view, register_view, logout_view)
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # If we use for url mapping view "import from" method
    # when we import some app view in directly
    # we can get conflict name
    # because all apps use views submodule
    # We can use more simple method to avoid this problem
    # we can wrap our view render function in quote, for example:
    # url(r'^<url>/<regexp>', '<appname>.views.<function>'),

    # or we can use this alias:
    # from <app> import views as <unique_alias_view>

    # if we use deeply urls we can to divide that in <appname><url> module
    url(r'^comments/', include('comments.urls', namespace='comments')),
    url(r'^login/', login_view, name='login'),
    url(r'^logout/', logout_view, name='logout'),
    url(r'^register/', register_view, name='register'),
    url(r'^', include('posts.urls', namespace='posts')),
    url(r'^api/posts/', include('posts.api.urls', namespace='posts-api')),
    url(r'^api/comments/', include('comments.api.urls', namespace='comments-api')),
    url(r'^api/users/', include('users.api.urls', namespace='users-api')),
    url(r'^api/auth/token/', obtain_jwt_token),
]

''' AUTH TOKEN:
Make token for user:
curl -X POST -d "username=cfe&password=learncode" http://127.0.0.1:8000/api/auth/token/

Get token
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImNmZSIsInVzZXJfaWQiOjEsImVtYWlsIjoiIiwiZXhwIjoxNDYxOTY1ODI5fQ.OTX7CZFZqxhaUnU9Da13Ebh9FY_bHMeCF1ypr9hXjWw

Check comments:
curl -H "Authorization: JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImNmZSIsInVzZXJfaWQiOjEsImVtYWlsIjoiIiwiZXhwIjoxNDYxOTY1ODI5fQ.OTX7CZFZqxhaUnU9Da13Ebh9FY_bHMeCF1ypr9hXjWw"
 http://127.0.0.1:8000/api/comments/

Create comment from JSON type:
curl -X POST
  -H "Authorization: JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImNmZSIsInVzZXJfaWQiOjEsImVtYWlsIjoiIiwiZXhwIjoxNDYxOTY2MTc4fQ._i5wEqJ_OO8wNiVVNAWNPGjGaO7OzChY0UzONgw06D0"
  -H "Content-Type: application/json"
  -d '{"content":"some reply to another try"}' 'http://127.0.0.1:8000/api/comments/create/?slug=new-title&type=post&parent_id=13'

'''

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
