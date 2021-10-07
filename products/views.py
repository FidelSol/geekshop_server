import random
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from products.models import ProductCategory, Product
from django.conf import settings
from django.core.cache import cache

def get_links_menu():
   if settings.LOW_CACHE:
       key = 'links_menu'
       links_menu = cache.get(key)
       if links_menu is None:
           links_menu = ProductCategory.objects.filter(is_active=True)
           cache.set(key, links_menu)
       return links_menu
   else:
       return ProductCategory.objects.filter(is_active=True)


def get_category(pk):
   if settings.LOW_CACHE:
       key = f'category_{pk}'
       category = cache.get(key)
       if category is None:
           category = get_object_or_404(ProductCategory, pk=pk)
           cache.set(key, category)
       return category
   else:
       return get_object_or_404(ProductCategory, pk=pk)


def get_products():
   if settings.LOW_CACHE:
       key = 'products'
       products = cache.get(key)
       if products is None:
           products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')
           cache.set(key, products)
       return products
   else:
       return Product.objects.filter(is_active=True, category__is_active=True).select_related('category')


def get_product(pk):
   if settings.LOW_CACHE:
       key = f'product_{pk}'
       product = cache.get(key)
       if product is None:
           product = get_object_or_404(Product, pk=pk)
           cache.set(key, product)
       return product
   else:
       return get_object_or_404(Product, pk=pk)


def get_products_orederd_by_price():
   if settings.LOW_CACHE:
       key = 'products_orederd_by_price'
       products = cache.get(key)
       if products is None:
           products = Product.objects.filter(is_active=True, category__is_active=True).order_by('price')
           cache.set(key, products)
       return products
   else:
       return Product.objects.filter(is_active=True, category__is_active=True).order_by('price')


def get_products_in_category_orederd_by_price(pk):
   if settings.LOW_CACHE:
       key = f'products_in_category_orederd_by_price_{pk}'
       products = cache.get(key)
       if products is None:
           products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')
           cache.set(key, products)
       return products
   else:
       return Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')

def get_hot_product():
   products = get_products()

   return random.sample(list(products), 1)[0]

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
class ProductList(ListView):
    model = Product
    context_object_name = "products"
    template_name = 'products/products.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(ProductList, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop - Каталог'
        context['categories'] = ProductCategory.objects.all()
        context['links_menu'] = get_links_menu()
        return context

    def get_queryset(self):
        category_id = self.kwargs.get('category_id', '')
        q = super().get_queryset()
        if category_id:
            category = get_category(category_id)
            result = get_products_in_category_orederd_by_price(category_id)
        else:
            result = get_products_orederd_by_price()
        return result

