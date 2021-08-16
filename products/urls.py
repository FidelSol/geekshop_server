from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^contact/$', views.contact, name='contact'),
    re_path(r'^products/$', views.products, name='products'),
]