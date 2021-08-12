from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('add', views.addHoneypot),
    path('remove', views.removeHoneypot),
    path('log/update', views.updateLog),
    path('log/get', views.getLog),
]