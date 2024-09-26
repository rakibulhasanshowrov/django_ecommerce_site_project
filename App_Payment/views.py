from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse
from django.contrib import messages
import string
#models and forms
from App_Order.models import Order, Cart
from App_Payment.forms import BillingAddress
from App_Payment.forms import BillingForm
from django.contrib.auth.decorators import login_required

# for payment
import requests
# from sslcommerz_python.payment import SSLCSession
from sslcommerz_lib import SSLCOMMERZ 
from decimal import Decimal
from sslcommerz_lib import SSLCOMMERZ
import socket
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@login_required
def checkout(request):
    saved_address = BillingAddress.objects.get_or_create(user=request.user)
    saved_address = saved_address[0]
    print(saved_address)
    form = BillingForm(instance=saved_address)
    if request.method == "POST":
        form = BillingForm(request.POST, instance=saved_address)
        if form.is_valid():
            form.save()
            form = BillingForm(instance=saved_address)
            messages.success(request, f"Shipping Address Saved!")
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    #print(order_qs)
    order_items = order_qs[0].orderitems.all()
    #print(order_items)
    order_total = order_qs[0].get_totals()
    return render(request, 'App_Payment/checkout.html', context={"form":form, "order_items":order_items, "order_total":order_total, "saved_address":saved_address})
  
  
@login_required
def payment(request):
    saved_address = BillingAddress.objects.get_or_create(user=request.user)
    saved_address = saved_address[0]
    if not saved_address.is_fully_filled():
        messages.info(request, f"Please complete shipping address!")
        return redirect("App_Payment:checkout")

    if not request.user.profile.is_fully_filled():
        messages.info(request, f"Please complete profile details!")
        return redirect("App_Login:profile")

    store_id = 'rhsli66f44960b03a6'
    API_key = 'rhsli66f44960b03a6@ssl'
    settings={ 'store_id': 'rhsli66f44960b03a6', 'store_pass': 'rhsli66f44960b03a6@ssl', 'issandbox': True }
    mypayment=SSLCOMMERZ(settings)
    

    status_url = request.build_absolute_uri(reverse("App_Payment:complete"))
    #print(status_url)
    

    order_qs = Order.objects.filter(user=request.user, ordered=False)
    print(f'Order_qs Result:{order_qs}')
    order_items = order_qs[0].orderitems.all()
    # order_items=[]
    # for item in order_items_cart:
    #     order_items.append(str(item))
    #     print(f'Items are:{str(item)}')
    print(f'Order_Items Result:{order_items}')
    order_items_count = order_qs[0].orderitems.count()
    print(f'Order Item Count:{order_items_count}')
    order_total = order_qs[0].get_totals()
    print(f'Order Total TK:{order_total}')
    current_user = request.user
    print(f'Current_user:{current_user}')
    post_data = {
    "total_amount": Decimal(order_total),
    "currency": "BDT",
    "tran_id": "221122",
    "product_category": "Mixed",
    "success_url": status_url,
    "fail_url": status_url,
    "cancel_url": status_url,
    "cus_name": current_user.profile.full_name,
    "cus_email": current_user.email,
    "shipping_method": 'NO',
    "num_of_item": order_items_count,
    "product_name": order_items[0],
    "product_category": 'Mixed',
    "product_profile": "physical-goods",
    "cus_add1": current_user.profile.address_1,
    "cus_city": current_user.profile.city,
    "cus_country": current_user.profile.country,
    "cus_phone": current_user.profile.phone,
}

    response_data = mypayment.createSession(post_data)
    print(response_data)
    
    return redirect(response_data['GatewayPageURL'])


@csrf_exempt
def complete(request):
    if request.method == 'POST' or request.method == 'post':
        payment_data = request.POST
        status = payment_data['status']
        if status == 'VALID':
            val_id = payment_data['val_id']
            tran_id = payment_data['tran_id']
            messages.success(request,f"Your Payment Completed Successfully! Page will be redirected!")
            return HttpResponseRedirect(reverse("App_Payment:purchase", kwargs={'val_id':val_id, 'tran_id':tran_id},))  
        elif status == 'FAILED':
            messages.warning(request, f"Your Payment Failed! Please Try Again! Page will be redirected!")
    return render(request,'App_Payment/complete.html',context={})


@login_required
def purchase(request, val_id, tran_id):
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order = order_qs[0]
    orderId = tran_id
    order.ordered = True
    order.orderId = orderId
    order.paymentId = val_id
    order.save()
    cart_items = Cart.objects.filter(user=request.user, purchased=False)
    for item in cart_items:
        item.purchased = True
        item.save()
    return HttpResponseRedirect(reverse("app_shop:home"))


def order_view(request):
    try:
        orders = Order.objects.filter(user=request.user, ordered=True)
        context = {"orders": orders}
    except:
        messages.warning(request, "You do no have an active order")
        return redirect("app_shop:home")
    return render(request, "App_Payment/order.html", context)
