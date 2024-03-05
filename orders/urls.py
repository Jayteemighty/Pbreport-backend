from django.urls import path
from orders import webhooks as wh
from orders import views

urlpatterns = [
    path('checkout/', views.checkout),
    path('orders/', views.OrdersList.as_view()),  
    path('webhook/', wh.paystack_webhook, name='paystack-webhook'),
]