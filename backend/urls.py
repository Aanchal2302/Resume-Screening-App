# classnest_Base/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import viewsets
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", viewsets.resume, name="resume"),
    path("pred", viewsets.pred, name="pred"),
]
