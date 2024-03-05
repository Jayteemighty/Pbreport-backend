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

    
