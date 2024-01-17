from django.shortcuts import render,redirect,HttpResponse
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced ,Review,Payment
from .forms import CustomerRegistrationForm,CustomerProfileForm, ReviewForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse  
from django.conf import settings
import razorpay
from django.shortcuts import get_object_or_404

# Now, you can access EMAIL_HOST_USER as settings.EMAIL_HOST_USER
email_host_user = settings.EMAIL_HOST_USER


# def home(request):
#  return render(request, 'app/home.html')

class ProductView(View):
 def get(self, request):
  topwears = Product.objects.filter(category='TW')
  bottomwears = Product.objects.filter(category='BW')
  mobiles = Product.objects.filter(category='M')
  laptop = Product.objects.filter(category='L')
  return render(request, 'app/home.html',{'topwears':topwears,'bottomwears':bottomwears,'mobiles':mobiles,'laptop':laptop})
  

# def product_detail(request):
#  return render(request, 'app/productdetail.html')


class ProductDetailView(View):
 def get(self, request, pk):
  product=Product.objects.get(pk=pk)
  reviews=Review.objects.filter(product=product)
  item_already_in_cart =False
  
  if request.user.is_authenticated:
   item_already_in_cart = Cart.objects.filter(Q(product=product.id)& Q(user=request.user)).exists()
  return render(request,'app/productdetail.html',{'product':product,'item_already_in_cart':item_already_in_cart,'reviews':reviews})

class ProductSearchView(View):
    def get(self, request):
        query = request.GET.get('query')  # Get the search query from the request
        products = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query)| Q(brand__icontains=query))
        # results = [{'id': product.id, 'title': product.title} for product in products]
        # return JsonResponse({'results': results})
        
        
        return render(request, 'app/search.html', {'products': products, 'query': query})




@login_required
def add_to_cart(request):
 user=request.user
 product_id=request.GET.get('prod_id')
 print(product_id) 
 product=Product.objects.get(id=product_id)
 Cart(user=user,product= product).save()
 return redirect('/cart')

@login_required
def show_cart(request):
 if request.user.is_authenticated:
  user=request.user
  cart=Cart.objects.filter(user=user)
  # print(cart)
  amount=00.00
  shipping_amount=60.00
  totalamount=00.00
  cart_product=[p for p in Cart.objects.all() if p.user==user]
  # print(cart_product)
  if cart_product:
   for p in cart_product:
    tempamount=(p.quantity*p.product.discounted_price)
    amount+= tempamount
    totalamount=amount+shipping_amount
   return render(request, 'app/addtocart.html',{'carts':cart,'totalamount':totalamount,'amount':amount})
  else:
   return render(request, 'app/emptycart.html',)
  
def plus_cart(request):
 if request.method=='GET':
  prod_id=request.GET['prod_id']
  c= Cart.objects.get(Q(product=prod_id)&Q(user=request.user))
  c.quantity+=1
  c.save()
  amount=00.00
  shipping_amount=60.00
  totalamount=00.00
  cart_product=[p for p in Cart.objects.all() if p.user==request.user]
  for p in cart_product:
    tempamount=(p.quantity*p.product.discounted_price)
    amount+= tempamount
    


  data={
     'quantity':c.quantity,
     'amount':amount,
     'totalamount':amount +shipping_amount
    }
  return JsonResponse(data)


def minus_cart(request):
 if request.method=='GET':
  prod_id=request.GET['prod_id']
  c= Cart.objects.get(Q(product=prod_id)&Q(user=request.user))
  c.quantity-=1
  c.save()
  amount=00.00
  shipping_amount=60.00
  totalamount=00.00
  cart_product=[p for p in Cart.objects.all() if p.user==request.user]
  for p in cart_product:
    tempamount=(p.quantity*p.product.discounted_price)
    amount+= tempamount
    


  data={
     'quantity':c.quantity,
     'amount':amount,
     'totalamount':amount +shipping_amount
    }
  return JsonResponse(data)
@login_required
def remove_cart(request):
 if request.method=='GET':
  prod_id=request.GET['prod_id']
  c= Cart.objects.get(Q(product=prod_id)&Q(user=request.user))
  
  c.delete()
  amount=00.00
  shipping_amount=60.00
  totalamount=00.00
  cart_product=[p for p in Cart.objects.all() if p.user==request.user]
  for p in cart_product:
    tempamount=(p.quantity*p.product.discounted_price)
    amount+= tempamount
    


  data={
     
     'amount':amount,
     'totalamount':amount +shipping_amount
    }
  return JsonResponse(data)

@login_required
def buy_now(request):
 return render(request, 'app/buynow.html')

# def profile(request):
#  return render(request, 'app/profile.html')
@login_required
def address(request):
 add = Customer.objects.filter(user=request.user)
 return render(request, 'app/address.html',{'add':add,'active':'btn-primary'})

@login_required
def orders(request):
 op = OrderPlaced.objects.filter(user=request.user)
 return render(request, 'app/orders.html',{'order_placed':op})

# def change_password(request):
#  return render(request, 'app/changepassword.html')

def mobile(request,data=None):
 if data == None:
  mobiles = Product.objects.filter(category='M')
 elif data=='Apple' or data=='Samsung':
  mobiles = Product.objects.filter(category='M').filter(brand=data)
 elif data=='below':
  mobiles = Product.objects.filter(category='M').filter(discounted_price_lt=90000)
 elif data=='above':
  mobiles = Product.objects.filter(category='M').filter(discounted_price_gt=90000) 
 return render(request, 'app/mobile.html',{'mobiles':mobiles})

def laptop(request,data=None):
 if data == None:
  laptop = Product.objects.filter(category='L')
 elif data=='Apple' or data=='Lenovo':
  laptop = Product.objects.filter(category='L').filter(brand=data)
 elif data=='below':
  laptop = Product.objects.filter(category='L').filter(discounted_price_lt=90000)
 elif data=='above':
  laptop = Product.objects.filter(category='L').filter(discounted_price_gt=90000) 
 return render(request, 'app/laptop.html',{'laptop':laptop})

def topwear(request,data=None):
 if data == None:
  topwears = Product.objects.filter(category='TW')
 elif data=='Adidas' or data=='Nike' or data=='Levi'or data=='Tommy Hilfigher': 
  topwears = Product.objects.filter(category='TW').filter(brand=data)
#  elif data=='below':
#   topwears = Product.objects.filter(category='TW').filter(discounted_price_lt=90000)
#  elif data=='above':
#   topwears = Product.objects.filter(category='TW').filter(discounted_price_gt=90000) 
 return render(request, 'app/topwear.html',{'topwears':topwears})

def bottomwear(request,data=None):
 if data == None:
  bottomwears = Product.objects.filter(category='BW')
 elif data=='Levi' or data=='calvin klien' or data=='wrangler':
  bottomwears = Product.objects.filter(category='BW').filter(brand=data)
#  elif data=='below':
#   bottomwears = Product.objects.filter(category='BW').filter(discounted_price_lt=90000)
#  elif data=='above':
#   bottomwears = Product.objects.filter(category='BW').filter(discounted_price_gt=90000) 
 return render(request, 'app/bottomwear.html',{'bottomwears':bottomwears})



# def login(request):
#  return render(request, 'app/login.html')

# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')


class CustomerRegistrationView(View):
 def get(self,request):
  form = CustomerRegistrationForm()
  return render(request, 'app/customerregistration.html',{'form':form})
 def post(self,request):
  form = CustomerRegistrationForm(request.POST)
  if form.is_valid():
   messages.success(request,'Congratulations !! Registered Successfully')
   form.save()
  return render(request, 'app/customerregistration.html',{'form':form})

@login_required
def checkout(request):
 user=request.user
 add =Customer.objects.filter(user=user)
 cart_items= Cart.objects.filter(user=user)
 amount=0.0
 shipping_amount=60.0
 totalamount=00.00
 cart_product=[p for p in Cart.objects.all() if p.user==request.user]
 
 if cart_product:
  for p in cart_product:
    tempamount=(p.quantity*p.product.discounted_price)
    amount+= tempamount
  totalamount=amount+shipping_amount
  razoramount =  int(totalamount*100)
  client = razorpay.Client(auth=(settings.RAZOR_KEY_ID,settings.RAZOR_KEY_SECRET))
  data={"amount":razoramount,"currency":"INR","receipt":"order_rcptid_11"}
  payment_response = client.order.create(data=data)
  print(payment_response)
  order_id = payment_response['id']
  order_status = payment_response['status']
  if order_status == 'created':
   payment = Payment(
    user=user,
    amount=totalamount,
    razorpay_order_id = order_id,
    razorpay_payment_status = order_status
   )
   payment.save() 


 return render(request, 'app/checkout.html', locals())





@login_required
def payment_done(request):
    order_id = request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')
    custid = request.GET.get('custid')
    user = request.user

    try:
        customer = Customer.objects.get(id=custid)
    except Customer.DoesNotExist:
        print("Error: Customer not found with the provided ID")
        return HttpResponse("Error: Customer not found with the provided ID")

    try:
        payment = Payment.objects.get(razorpay_order_id=order_id)
    except Payment.DoesNotExist:
        print("Error: Payment not found with the provided order ID")
        return HttpResponse("Error: Payment not found with the provided order ID")

    payment.paid = True
    payment.razorpay_payment_id = payment_id
    payment.save()

    cart = Cart.objects.filter(user=user)

    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity, payment=payment).save()
        c.delete()

    return redirect("orders")

# @login_required
# def payment_done(request):
#  order_id = request.GET.get('order_id')
#  print("order_id:",order_id)
#  payment_id = request.GET.get('payment_id')
#  print("payment_id:",payment_id)
#  user=request.user
#  custid = request.GET.get('custid')
#  customer=Customer.objects.get(id = custid)
#  print("custid:", custid)

#  payment=Payment.objects.get(razorpay_order_id=order_id)
#  payment.paid=True
#  payment.razorpay_payment_id = payment_id
#  payment.save()
#  cart=Cart.objects.filter(user=user)
#  for c in cart:
#     OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity,payment=payment).save()
#     c.delete()
# #   order_id = OrderPlaced.objects.latest('id').id  # Get the ID of the latest order
# #   generate_invoice_url = reverse('generateinvoice', kwargs={'pk': order_id})
# # #   return redirect(generate_invoice_url)
#  return redirect("orders")  

@method_decorator(login_required,name='dispatch')
class ProfileView(View):
 def get(self,request):
  form=CustomerProfileForm()
  return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})
 def post(self,request):
  form=CustomerProfileForm(request.POST)
  if form.is_valid():
   usr= request.user
   name=form.cleaned_data['name']
   locality=form.cleaned_data['locality']
   city=form.cleaned_data['city']
   state=form.cleaned_data['state']
   zipcode=form.cleaned_data['zipcode']
   reg=Customer(user=usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
   reg.save()
   messages.success(request,'Congratulations!! Profile Updated Successfully')
  return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})

#  def Review_rate(request):
#   if request.method == "GET":
#    prod_id=request.GET.get('prod_id')
#    product=Product.objects.get(id=prod_id)
#    comment=request.Get.get('comment')
#    rate=request.Get.get('rate')
#    user=request.user
#    if request.method == "POST":
#     rate=request.POST.get('rate')
#     comment=request.POST.get('comment')
   
#    Review(user=user,product=product,comment=comment,rate=rate).save()
#    review=Review.objects.get('')
#    return redirect('product-detail',id=prod_id)

def submit_review(request,prod_id):
 url= request.META.get('HTTP_REFERER')
 if request.method=='POST':
  try:
   reviews=Review.objects.get(user__id=request.user.id,product__id=prod_id)
   form= ReviewForm(request.POST,instance=reviews)
   form.save() 
   messages.success(request,'Thank you! Your review has been updated.')
   return redirect(url)
  except Review.DoesNotExist:
   form=ReviewForm(request.POST)
   if form.is_valid():
    data=Review()
    data.subject=form.cleaned_data['subject']
    data.rating=form.cleaned_data['rating']
    data.comment=form.cleaned_data['comment']
    data.ip=request.META.get('REMOTE_ADDR')
    data.product_id=prod_id
    data.user_id=request.user.id
    data.save()
    messages.success(request,'Thank you! Your review has been submitted.')
    return redirect(url)
     

# # for generating pdf invoice
 from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

def generate_pdf_invoice(request, transaction_id, product_id):
    try:
        transaction = RazorpayTransaction.objects.get(id=transaction_id)
        product = Product.objects.get(id=product_id)
    except RazorpayTransaction.DoesNotExist or Product.DoesNotExist:
        # Handle the case where the transaction or product does not exist
        return render(request, 'app/error_page.html', {'message': 'Transaction or product not found'})

    # Create a response object
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{transaction_id}.pdf"'

    # Create a template context
    context = {
        'transaction': transaction,
        'product': product,
    }

    # Render the template to HTML
    template = get_template('app/pdf_invoice_template.html')
    html = template.render(context)

    # Create the PDF using xhtml2pdf
    pdf = pisa.pisaDocument(html, response)

    if not pdf.err:
        return response

    return HttpResponse('Error generating PDF', content_type='text/plain')

def payment_success_callback(request):
    # Verify the payment status from the Razorpay callback data
    # Parse the transaction_id and product_id from the callback data
    
    # Assuming you have fetched the necessary data, generate the invoice
    # You can use a library like xhtml2pdf or ReportLab to create a PDF invoice
    
    # Save the invoice details to the database (e.g., Invoice model)
    
    # Redirect the user to the payment success page
    return redirect('paymentsuccess')

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import os

def fetch_resources(uri, rel):
    path = os.path.join(uri.replace(settings.STATIC_URL, ""))
    return path

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)#, link_callback=fetch_resources)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None 


# from django.core.mail import EmailMultiAlternatives
# import razorpay

# razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

@csrf_exempt
def handlerequest(request):
    if request.method == "POST":
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            order_id = request.POST.get('razorpay_order_id','')
           
            params_dict = { 
            'razorpay_order_id': order_id, 
            'razorpay_payment_id': payment_id
            
            }
            try:
                orderplaced_db = OrderPlaced.objects.get(razorpay_order_id=id)
            except:
                return HttpResponse("505 Not Found")
            orderplaced_db.razorpay_payment_id = payment_id
            orderplaced_db.razorpay_signature = signature
            orderplaced_db.save()
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            if result==None:
                amount = orderplaced_db.total_amount * 100   #we have to pass in paisa
                try:
                    razorpay_client.payment.capture(payment_id, amount)
                    orderplaced_db.payment_status = 1
                    orderplaced_db.save()

                    ## For generating Invoice PDF
                    template = get_template('app/invoice.html')
                    data = {
                        'order_id': orderplaced_db.id,
                        'transaction_id': orderplaced_db.razorpay_payment_id,
                        'user_email': orderplaced_db.user.email,
                        'date': str(orderplaced_db.datetime_of_payment),
                        'name': orderplaced_db.user.name,
                        'order': orderplaced_db,
                        'amount': orderplaced_db.total_amount,
                    }
                    html  = template.render(data)
                    result = BytesIO()
                    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)#, link_callback=fetch_resources)
                    pdf = result.getvalue()
                    filename = 'Invoice_' + data['orderplaced_id'] + '.pdf'

                    mail_subject = 'Recent Order Details'
                    # message = render_to_string('app/orders/emailinvoice.html', {
                    #     'user': orderplaced_db.user,
                    #     'order': orderplaced_db
                    # })
                    context_dict = {
                        'user': orderplaced_db.user,
                        'order': orderplaced_db
                    }
                    template = get_template('app/orders/emailinvoice.html')
                    message  = template.render(context_dict)
                    to_email = orderplaced_db.user.email
                    # email = EmailMessage(
                    #     mail_subject,
                    #     message, 
                    #     settings.EMAIL_HOST_USER,
                    #     [to_email]
                    # )

                    # for including css(only inline css works) in mail and remove autoescape off
                    email = EmailMultiAlternatives(
                        mail_subject,
                        "hello",       # necessary to pass some message here
                        settings.EMAIL_HOST_USER,
                        [to_email]
                    )
                    email.attach_alternative(message, "text/html")
                    email.attach(filename, pdf, 'application/pdf')
                    email.send(fail_silently=False)

                    return render(request, 'app/paymentsuccess.html',{'id':orderplaced_db.id})
                except:
                    orderplaced_db.payment_status = 2
                    orderplaced_db.save()
                    return render(request, 'app/paymentfailed.html')
            else:
                orderplaced_db.payment_status = 2
                orderplaced_db.save()
                return render(request, 'app/paymentfailed.html')
        except:
            return HttpResponse("505 not found")

# class HandleRequestView(View):
#     @csrf_exempt
#     def post(self, request):
#         if request.method == "POST":
#             try:
#                 payment_id = request.POST.get('razorpay_payment_id', '')
#                 order_id = request.POST.get('razorpay_order_id', '')
#                 signature = request.POST.get('razorpay_signature', '')
#                 params_dict = {
#                     'razorpay_order_id': order_id,
#                     'razorpay_payment_id': payment_id,
#                     'razorpay_signature': signature
#                 }

#                 try:
#                     orderplaced_db = OrderPlaced.objects.get(razorpay_order_id=order_id)
#                 except OrderPlaced.DoesNotExist:
#                     return HttpResponse("505 Not Found")

#                 orderplaced_db.razorpay_payment_id = payment_id
#                 orderplaced_db.razorpay_signature = signature
#                 orderplaced_db.save()
#                 result = razorpay_client.utility.verify_payment_signature(params_dict)

#                 if result is None:
#                     amount = orderplaced_db.total_amount * 100  # Amount should be in paisa

#                     try:
#                         razorpay_client.payment.capture(payment_id, amount)
#                         orderplaced_db.payment_status = 1
#                         orderplaced_db.save()

#                         # Generate Invoice PDF
#                         template = get_template('app/invoice.html')
#                         data = {
#                             'order_id': orderplaced_db.id,
#                             'transaction_id': orderplaced_db.razorpay_payment_id,
#                             'user_email': orderplaced_db.user.email,
#                             'date': str(orderplaced_db.datetime_of_payment),
#                             'name': orderplaced_db.user.name,
#                             'order': orderplaced_db,
#                             'amount': orderplaced_db.total_amount,
#                         }
#                         html = template.render(data)
#                         result = BytesIO()
#                         pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
#                         pdf = result.getvalue()
#                         filename = f'Invoice_{orderplaced_db.id}.pdf'

#                         mail_subject = 'Recent Order Details'
#                         context_dict = {
#                             'user': orderplaced_db.user,
#                             'order': orderplaced_db
#                         }
#                         template = get_template('app/emailinvoice.html')
#                         message = template.render(context_dict)
#                         to_email = orderplaced_db.user.email

#                         email = EmailMultiAlternatives(
#                             mail_subject,
#                             "hello",
#                             settings.EMAIL_HOST_USER,
#                             [to_email]
#                         )
#                         email.attach_alternative(message, "text/html")
#                         email.attach(filename, pdf, 'application/pdf')
#                         email.send(fail_silently=False)

#                         return render(request, 'app/paymentsuccess.html', {'id': orderplaced_db.id})
#                     except Exception as e:
#                         orderplaced_db.payment_status = 2
#                         orderplaced_db.save()
#                         return render(request, 'app/paymentfailed.html')
#                 else:
#                     orderplaced_db.payment_status = 2
#                     orderplaced_db.save()
#                     return render(request, 'app/paymentfailed.html')
#             except Exception as e:
#                 return HttpResponse("505 not found")

class GenerateInvoice(View):
    def get(self, request, pk, *args, **kwargs):
        try:
            orderplaced_db = OrderPlaced.objects.get(id=pk, user=request.user, payment_status=1)
        except OrderPlaced.DoesNotExist:
            return HttpResponse("505 Not Found")

        data = {
            'order_id': orderplaced_db.id,
            'transaction_id': orderplaced_db.razorpay_payment_id,
            'user_email': orderplaced_db.user.email,
            'date': str(orderplaced_db.ordered_date),
            'name': orderplaced_db.user.name,
            'order': orderplaced_db,
            'amount': orderplaced_db.total_amount,
        }
        pdf = render_to_pdf('app/invoice.html', data)

        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = f"Invoice_{data['order_id']}.pdf"
            content = f"attachment; filename={filename}"
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")


# # class GenerateInvoice(View):
# #     def get(self, request, pk, *args, **kwargs):
# #         try:
# #             orderplaced_db = OrderPlaced.objects.get(id = pk, user = request.user, payment_status = 1)     #you can filter using order_id as well
# #         except:
# #             return HttpResponse("505 Not Found")
# #         data = {
# #             'order_id': orderplaced_db.id,
# #             'transaction_id': orderplaced_db.razorpay_payment_id,
# #             'user_email': orderplaced_db.user.email,
# #             'date': str(orderplaced_db.datetime_of_payment),
# #             'name': orderplaced_db.user.name,
# #             'order': orderplaced_db,
# #             'amount': orderplaced_db.total_amount,
# #         }
# #         pdf = render_to_pdf('app/invoice.html', data)
# #         #return HttpResponse(pdf, content_type='application/pdf')

# #         # force download
# #         if pdf:
# #             response = HttpResponse(pdf, content_type='application/pdf')
# #             filename = "Invoice_%s.pdf" %(data['order_id'])
# #             content = "inline; filename='%s'" %(filename)
# #             #download = request.GET.get("download")
# #             #if download:
# #             content = "attachment; filename=%s" %(filename)
# #             response['Content-Disposition'] = content
# #             return response
# #         return HttpResponse("Not found")



