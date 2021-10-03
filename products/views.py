import json
from urllib.request import urlopen

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.apps import apps
from django.urls import reverse
from django.views.generic import ListView

from products.models import ProductCategory, Product


# index
@login_required
def index(request):
    context = {'title': 'GeekShop'}
    return render(request, 'products/index.html', context)

# contact
@login_required
def contact(request):
    context = {'title': 'GeekShop - Контакты'}
    return render(request, 'products/contact.html', context)

# products
# @login_required
# def products(request, category_id=None, page=1):
#     context = {'title': 'GeekShop - Каталог', 'categories': ProductCategory.objects.all()}
#     products = Product.objects.filter(category_id=category_id) if category_id else Product.objects.all()
#
#     paginator = Paginator(products, per_page=3)
#     try:
#         products_paginator = paginator.page(page)
#     except PageNotAnInteger:
#         products_paginator = paginator.page(1)
#     except EmptyPage:
#         products_paginator = paginator.page(paginator.num_pages)
#     context['products'] = products_paginator
#     return render(request, 'products/products.html', context)

# products
class ProductList(ListView):
    model = Product
    context_object_name = "products"
    template_name = 'products/products.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(ProductList, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop - Каталог'
        context['categories'] = ProductCategory.objects.all()
        return context

    def get_queryset(self):
        category_id = self.kwargs.get('category_id', '')
        q = super().get_queryset()
        if category_id:
            result = q.filter(category_id=category_id)
        else:
            result = q
        return result

def get_product_price(request, pk):
   if request.is_ajax():
       product = Product.objects.filter(pk=int(pk)).first()
       if product:
           return JsonResponse({'price': product.price})
       else:
           return JsonResponse({'price': 0})