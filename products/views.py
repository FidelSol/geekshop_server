import json
from urllib.request import urlopen

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.apps import apps
from django.urls import reverse

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

# index
@login_required
def products(request, category_id=None, page=1):
    context = {'title': 'GeekShop - Каталог', 'categories': ProductCategory.objects.all()}
    products = Product.objects.filter(category_id=category_id) if category_id else Product.objects.all()

    paginator = Paginator(products, per_page=3)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)
    context['products'] = products_paginator
    return render(request, 'products/products.html', context)

