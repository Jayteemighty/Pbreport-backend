import hmac
import hashlib
import json
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Order

secret = settings.PAYSTACK_SECRET_KEY

@csrf_exempt
def paystack_webhook(request):
    # Retrieve the payload from the request body
    payload = request.body
    # Signature header to verify the request is from Paystack
    sig_header = request.headers['x-paystack-signature']
    body = None
    event = None

    try:
        # Sign the payload with HMAC SHA512
        hash = hmac.new(secret.encode('utf-8'), payload, digestmod=hashlib.sha512).hexdigest()
        # Compare our signature with Paystack's signature
        if hash == sig_header:
            # If signature matches, proceed to retrieve event status from payload
            body_unicode = payload.decode('utf-8')
            body = json.loads(body_unicode)
            # Event status
            event = body['event']
        else:
            raise Exception
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except KeyError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except:
        # Invalid signature
        return HttpResponse(status=400)

    if event == 'charge.success':
        # If event status equals 'charge.success'
        # Get the data and the `order_id` 
        # we'd set in the metadata earlier
        data, order_id = body["data"], body['data']['metadata']['order_id']

        # Validate status and gateway_response
        if (data["status"] == 'success') and (data["gateway_response"] == "Successful"):
            try:
                order = Order.objects.get(id=order_id)
            except Order.DoesNotExist:
                return HttpResponse(status=404)
            # Mark order as paid
            order.paid_amount = data["amount"] / 100  # Convert from kobo to naira
            order.save(update_fields=["paid_amount"])

            print("Order marked as paid")

    return HttpResponse(status=200)
