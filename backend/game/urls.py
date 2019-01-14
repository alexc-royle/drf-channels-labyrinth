from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^create$', views.GameCreate.as_view(), name='game-create'),
]
