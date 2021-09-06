from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('products/', views.ProductList.as_view(), name='products'),
    # path('page/<int:page>/', views.products, name='page'),

]