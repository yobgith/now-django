from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from carts.models import CartItem
from store.models import Product
from .forms import OrderForm
import datetime
from .models import Order, Payment, OrderProduct
import json
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

def payments(request):
    
   # Store transaction détails inside Payment model
   if request.method == "POST":
    
        orders = Order.objects.filter(user=request.user)
        if 'payment_choice' in request.POST:
            ms = ['Cash on delivery', 'Wave', 'Mobile Money']
            payment_chois = request.POST.getlist('payment')

            if payment_chois == ['Cash on delivery']:
                for order in orders:
                    Payment.objects.create(
                        user = order.user,
                        payment_id = order.order_number,
                        payment_method = request.POST.get("payment"),
                        amount_paid = order.order_total, 
                        status = "à la Reception",
                )
                order.is_ordered = True
                order.save()


    
        # Move the cart items to Order Product table
                # products = Product.objects.get.filter(product = request.product_id)
                cart_items = CartItem.objects.filter(user=request.user)
                for item in cart_items:
                    orderproduct = OrderProduct()
                    orderproduct.order_id = order.id
                    orderproduct.payment = order.payment
                    orderproduct.user = request.user
                    orderproduct.product_id = item.product_id
                    orderproduct.quantity = item.quantity
                    orderproduct.product_price = item.product.price
                    orderproduct.ordered = True
                    orderproduct.save()
                    
                
            # le scrypte d'Origine
                # orderproduct = OrderProduct()
                #     orderproduct.order_id = order.id                OK
                #     orderproduct.payment = payment                    NO 
                #     orderproduct.user = request.user.id               ~
                #     orderproduct.product_id = item.product_id         OK
                #     orderproduct.quantity = item.quantity             OK
                #     orderproduct.product_price = item.product.price   OK
                #     orderproduct.ordered = True                       OK
                #     orderproduct.save()                               OK


                    Cart_item = CartItem.objects.get(id=item.id)
                    product_variation = Cart_item.variations.all()

                    orderproduct = OrderProduct.objects.get(id=orderproduct.id)
                    orderproduct.variations.set(product_variation)
                    orderproduct.save()



            # Reduce the quantite of the sold products

                    product = Product.objects.get(id=item.product_id)
                    product.stock -= item.quantity
                    product.save()

            # Clear cart

                CartItem.objects.filter(user=request.user).delete()

            # Send order recieeved email to customer

                mail_subject = "Merci pour votre commande !"
                message = render_to_string('orders/order_recieved_email.html', {
                    "user": request.user,
                    "order" : order,
                })
                to_email = request.user.email
                send_email = EmailMessage(mail_subject, message, to=[to_email])
                send_email.send()

            # Send order number and transaction id back to senData method via JsonReponse
                ordered_products = OrderProduct.objects.filter(order_id=order.id)
                subtotal = 0
                for i in ordered_products:
                    subtotal += i.product_price * i.quantity


                context = {
                    "order_number": order.order_number,
                    "transID": Payment,
                    'order' : order,
                    'ordered_products': ordered_products,
                    'subtotal': subtotal,
                    
                }
            

                #return redirect('order_complete')
                return render(request, 'orders/order_complete.html', context)



def place_order(request, total=0, quantity=0,):
    current_user = request.user

    #if the count is less than or equal to 0, then redirect back to shop
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <=0:
        return redirect('store')
    
    
    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2 * total)/100
    grand_total = total + tax  

    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        
        if form.is_valid() :
            # HttpResponse
            # Store all the billing information inside Order table
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d") #20210305
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            context = {
            'order': order,
            'cart_items':cart_items,
            'total':total,
            'tax':tax,
            'grand_total':grand_total,
            }
        
        return render(request, 'orders/payments.html', context)
        

    else:
        return redirect('checkout')



def order_complete(request):
    
    return render(request, 'orders/order_complete.html')



















# if request.method == "POST":
#         if 'payment_choice' in request.POST:
#             ms = ['Cash on delivery', 'Wave', 'Mobile Money']
#             payment_chois = request.POST.getlist('payment')

#             if payment_chois == ['Cash on delivery']:
#                  for ord in order:
#                     payment = Payment(
#                     user = request.user,
#                     payment_id = request.order_number,
#                     payment_method = request.POST.get("payment"),
#                     amount_paid = Order.order_total ,
#                     status = "à la Reception",
#                     )
#                     payment.save()
#             order = Order(
#                 is_ordered = True
#                 )
#                 # order.save()           

#             if payment_chois == ['Wave']:
#                 payment = Payment(
#                     user = request.user,
#                     payment_id = "payman1",
#                     payment_method = request.POST.get("payment"),
#                     amount_paid = order.order_total, 
#                     stattus = request.POST.get("payment"),
#                     )
#                 payment.save()

#             if payment_chois == ['Mobile Money']:
#                 payment = Payment(
#                     user = request.id,
#                     payment_id = "payman1",
#                     payment_method = request.POST.get("payment"),
#                     amount_paid = order.order_total, 
#                     stattus = request.POST.get("payment"),
#                     )
#                 payment.save()
            
#                 order.payment = payment
#                 order.is_ordered = True
#                 order.save()
#                 return render(request, 'orders/payments.html')
#                 order = Order()
#                 print("gggggggggggggggggggggggggggggggggggggggggg")
#                 order.is_ordered = True
#                 order.save()
#                 return render(request, 'orders/payments.html')
            