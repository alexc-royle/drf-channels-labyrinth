from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^create$', views.UserCreate.as_view(), name='account-create'),
]
