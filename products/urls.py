from django.urls import path, re_path
from django.views.decorators.cache import cache_page

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('products/', cache_page(3600) (views.ProductList.as_view()), name='products'),
    # path('page/<int:page>/', views.products, name='page'),

]