from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import HttpResponseRedirect
from django.template.loader import render_to_string

from products.models import Product
from baskets.models import Basket

@login_required
def basket_add(request):
    if request.is_ajax():
        product_id = request.GET.get('product_id', None)
        if product_id:
            product = Product.objects.get(id=int(product_id))
            baskets = Basket.objects.filter(user=request.user, product=product)

            if not baskets.exists():
                Basket.objects.create(user=request.user, product=product, quantity=1)
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                basket = baskets.first()
                basket.quantity = F('quantity') + 1
                basket.save()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_remove(request, id):
    basket = Basket.objects.get(id=id)
    basket.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def basket_edit(request):
    if request.is_ajax():
        quantity = request.GET.get('quantity', None)
        id = request.GET.get('id', None)
        if id and quantity:
            quantity = int(quantity)
            id = int(id)
            basket = Basket.objects.get(id=id)
            if quantity > 0:
                basket.quantity = quantity
                basket.save()
            else:
                basket.delete()
            baskets = Basket.objects.filter(user=request.user)
            context = {'baskets': baskets}
            result = render_to_string('baskets/baskets.html', context)
            return JsonResponse({'result': result})
        else:
            return JsonResponse({'status': 500})
