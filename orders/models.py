from django.db import models
from django.conf import settings
import requests
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
        # Paystack API endpoint for verifying transactions
        PAYSTACK_VERIFY_URL = 'https://api.paystack.co/transaction/verify/'

        # Set your Paystack secret key from Django settings
        paystack_secret_key = settings.PAYSTACK_SECRET_KEY

        # Make a request to the Paystack API to verify the transaction
        response = requests.get(PAYSTACK_VERIFY_URL + reference, headers={
            'Authorization': f'Bearer {paystack_secret_key}'
        })

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()
            # Check if the transaction was successful
            if data['data']['status'] == 'success':
                # Update the order details
                self.payment_verified = True
                self.paid_amount = data['data']['amount'] / 100  # Paystack amount is in kobo, so divide by 100
                self.save()
                return True  # Payment verified successfully
            else:
                return False  # Payment verification failed
        else:
            return False  # Payment verification failed

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return '%s' % self.id