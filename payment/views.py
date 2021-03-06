from decimal import Decimal
from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from paypal.standard.forms import PayPalPaymentsForm
from orders.models import Order
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

@login_required
def payment_process(request):
    print('start payment')
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    host = request.get_host()
    print('After getting data')
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '%.2f' % Decimal(order.get_total_cost()).quantize(Decimal('.01')),
        'item_name': 'Order {}'.format(order.id),
        'invoice': str(order.id),
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host,reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,reverse('payment:done')),
        'cancel_return': 'http://{}{}'.format(host,reverse('payment:canceled')),
    }
    print(paypal_dict)
    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request,
              'payment/process.html',{'order': order, 'form':form})
@csrf_exempt
@login_required
def payment_done(request):
    return render(request, 'payment/done.html')
@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment/canceled.html')