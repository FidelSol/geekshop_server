from django.contrib.auth.decorators import login_required
from django.urls import path
from orders.views import OrderList, order_forming_complete, OrderItemsCreate, OrderRead, OrderItemsUpdate, OrderDelete

app_name = 'orders'

urlpatterns = [
    path('', login_required(OrderList.as_view()), name='orders_list'),
    path('forming/complete/<int:pk>/', order_forming_complete, name='order_forming_complete'),
    path('create/', login_required(OrderItemsCreate.as_view()), name='order_create'),
    path('read/<int:pk>/', login_required(OrderRead.as_view()), name='order_read'),
    path('update/<int:pk>/', login_required(OrderItemsUpdate.as_view()), name='order_update'),
    path('delete/<int:pk>/', login_required(OrderDelete.as_view()), name='order_delete'),
]