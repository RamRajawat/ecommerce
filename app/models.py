from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator
from django.utils import timezone
from datetime import timedelta
from django.core.validators import RegexValidator
# from multiselectfield import MultiSelectField


# Create your models here.
STATE_CHOICES =(
    ('Andaman & Nicobar Island','Andaman & Nicobar Island'),
    ('Andhra Pradesh','Andhra Pradesh'),
    ('Arunachal Pradesh','Arunachal Pradesh'),
    ('Assam','Assam'),
    ('Bihar','Bihar'),
    ('Chandigarh','Chandigarh'),
    ('Chattisgarh','Chattisgarh'),
    ('Dadara and Nagar Haveli','Dadara and Nagar Haveli'),
    ("Delhi",'Delhi'),
    ('Goa','Goa'),
    ('Gujarat','Gujarat'),
    ('Haryana','Haryana'),
    ('Himachali Pradesh','Himachali Pradesh'),
    ('Jammu and Kashmir','Jammu and Kashmir'),
    ('Jharkhand','Jharkhand'),
    ('Karnataka','Karnataka'),
    ('Kerala','Kerala'),
    ('Lakshadweep','Lakshadweep'),
    ('Madhya Pradesh','Madhya Pradesh'),
    ('Maharashtra','Maharashtra'),
    ('Manipur','Manipur'),
    ('Meghalaya','Meghalaya'),
    ('Mizoram','Mizoram'),
    ('Nagaland','Nagaland'),
    ('Odisha','Odisha'),
    ('Puducherry','Puducherry'),
    ('Punjab','Punjab'),
    ('Rajasthan','Rajasthan'),
    ('Sikkim','Sikkim'),
    ('Tamilnadu','Tamilnadu'),
    ('Telangana','Telangana'),
    ('Tripura','Tripura'),
    ('Uttarakhand','Uttarakhand'),
    ('Uttar Pradesh','Uttar Pradesh'),
    ('West Bengal','West Bengal'),
    
)

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES,max_length=50)
    
    def __str__(self):
     return str(self.id)
    
CATEGORY_CHOICES =(
   ('M','Mobile'),
   ('L','Laptop'),
   ('TW', 'Top Wear') ,
   ('BW','Bottom Wear'),

)    
     
class Product(models.Model):
   title = models.CharField(max_length=100)
   selling_price = models.FloatField()
   discounted_price = models.FloatField()
   description = models.TextField()
   brand = models.CharField(max_length=100)
   category  = models.CharField ( choices= CATEGORY_CHOICES ,max_length=2)
   product_image = models.ImageField(upload_to='productimg')

   def __str__(self):
      return str(self.id)
   
class Cart(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   product = models.ForeignKey(Product, on_delete=models.CASCADE)
   quantity = models.PositiveIntegerField (default=1)

   def __str__(self):
      return str(self.id)
   
   @property
   def total_cost(self):
      return self.quantity*self.product.discounted_price
   

STATUS_CHOICES = (
   ('Accepted','Accepted'),
   ('Packed', 'Packed'),
   ('On The Way','On The Way'),
   ("Delivered", "Delivered"),
   ('Cancel','Cancel'),
   ('Pending','Pending')
)

payment_status_choices = (
        (1, 'SUCCESS'),
        (2, 'FAILURE' ),
        (3, 'PENDING'),
    )


class Payment(models.Model):
    
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    amount = models.FloatField()
    razorpay_order_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_payment_status = models.CharField(max_length=100, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=100, null=True, blank=True)
    paid = models.BooleanField(default=False)
   

class OrderPlaced(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
   product = models.ForeignKey(Product, on_delete=models.CASCADE)
   quantity = models.PositiveIntegerField(default=1)
   ordered_date = models.DateTimeField(auto_now_add=True)
   status   = models.CharField( max_length=15, choices= STATUS_CHOICES ,default='Pending')
   payment = models.ForeignKey(Payment,on_delete=models.CASCADE, default='')
#    datetime_of_payment = models.DateTimeField(default=timezone.now)
#    total_amount = models.FloatField(default=0.0)
#    payment_status = models.IntegerField(choices = payment_status_choices, default=3)
   
#    #related to razorpay
#    razorpay_order_id = models.CharField(max_length=500, null=True, blank=True)
#    razorpay_payment_id = models.CharField(max_length=500, null=True, blank=True)
#    razorpay_signature = models.CharField(max_length=500, null=True, blank=True)
    
   @property
   def total_cost(self):
      return self.quantity*self.product.discounted_price
   
#    def save(self, *args, **kwargs):
#         if self.id is None and self.datetime_of_payment and self.id:
#             self.id = self.datetime_of_payment.strftime('PAY2ME%Y%m%dODR') + str(self.id)
#         return super().save(*args, **kwargs)
   
#    def __str__(self):
#         return self.user.email + " " + str(self.id)



# class ProductInOrderPlaced(models.Model):
#     class Meta:
#         unique_together = (('order', 'product'),)
#     order = models.ForeignKey(OrderPlaced, on_delete = models.CASCADE)
#     product = models.ForeignKey(Product, on_delete = models.CASCADE)
#     quantity = models.PositiveIntegerField()
#     total_amount = models.FloatField(default=0.0)


class OtpModel(models.Model):
    otp_regex = RegexValidator( regex = r'^\d{6}$',message = "otp should be in six digits")
    otp = models.CharField(max_length=6, validators=[otp_regex])
    phone_regex = RegexValidator( regex = r'^\d{10}$',message = "phone number should exactly be in 10 digits")
    phone = models.CharField(max_length=255, validators=[phone_regex])
    expiry = models.DateTimeField(default = (timezone.now() + timedelta(minutes = 5)))
    is_verified = models.BooleanField(default=False)
    


class Review(models.Model):  
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   product = models.ForeignKey(Product, on_delete=models.CASCADE) 
   subject=models.CharField(max_length=100,blank=True)
   comment = models.TextField(max_length=350,blank=True) 
   rating = models.FloatField(default=0)
   ip=models.CharField(max_length=20,blank=True)
   status=models.BooleanField(default=True)
   created_at = models.DateTimeField(auto_now_add=True)  
   updated_at = models.DateTimeField(auto_now=True)  

   def __str__(self): 
      return self.subject
   

class CustomPermissions(models.Model):

    class Meta:

        managed = False  # No database table creation or deletion  \
                         # operations will be performed for this model.

        default_permissions = () # disable "add", "change", "delete"
                                 # and "view" default permissions

        # All the custom permissions not related to models on Manufacturer
        permissions = (
            ('accept_order', 'can accept order'),
            ('reject_order', 'can reject order'),
            ('view_order', 'can view order'),
            ('change_order', 'can change order'),
            ('view_return', 'can view return'),
            ('accept_return', 'can accept return'),
            ('reject_return', 'can reject return'),
            ('change_return', 'can change return'),
            ('view_dashboard', 'can view dashboard'),
        )

    
       