from django.contrib import admin
from django.contrib.sessions.models import Session
import pprint

from .models import(
    Customer,
    Product,
    Cart,
    Payment,
    OrderPlaced,
    Review,
    # ProductInOrderPlaced,
    OtpModel,
    
)

# Register your models here.

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id','user','name','locality','city','zipcode','state']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=['id','title','selling_price','discounted_price','description','brand','category','product_image']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display=['id','user','product','quantity']



@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display=['id','user','amount','razorpay_order_id','razorpay_payment_status','razorpay_payment_id','paid']


@admin.register(OrderPlaced)
class OrderPlacedAdmin(admin.ModelAdmin):
    list_display=['id','user','customer','product','quantity','ordered_date','status','payment']



@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display=['id','user','product','rating','subject','comment','ip','created_at','updated_at']    

class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return pprint.pformat(obj.get_decoded()).replace('\n', '<br>\n')
    _session_data.allow_tags=True
    list_display = ['session_key', '_session_data', 'expire_date']
    readonly_fields = ['_session_data']
    exclude = ['session_data']

admin.site.register(Session, SessionAdmin)

# admin.site.register(ProductInOrderPlaced)
admin.site.register(OtpModel)
