from django.db import models
from django.conf import settings
import secrets
from products.models import Product

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='orders', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_amount = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    paystack_reference = models.CharField(max_length=255, blank=True, null=True)
    payment_verified = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at',]
    
    def __str__(self):
        return self.first_name
    
    def save(self, *args, **kwargs):
        if not self.pk:  # Check if the order is being created
            while not self.ref:
                ref = secrets.token_urlsafe(50)
                object_with_similar_ref = Order.objects.filter(ref=ref)
                if not object_with_similar_ref:
                    self.ref = ref
        super().save(*args, **kwargs)
        
    def amount_value(self):
        return self.amount * 100

    def verify_payment(self, reference):
        # Logic to verify payment with Paystack API using the provided reference
        # If payment is successful, set payment_verified to True and update paid_amount
        # You need to implement this method based on your Paystack integration strategy
        pass

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return '%s' % self.id