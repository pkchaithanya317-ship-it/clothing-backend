from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class user_table(models.Model):
    LOGIN=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    phone=models.BigIntegerField()
    address=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    pincode=models.IntegerField()
class category_table(models.Model):
    name=models.CharField(max_length=100)
    category=models.CharField(max_length=100)
    def __str__(self):
        return self.name
    


class product_table(models.Model):
    CATEGORY=models.ForeignKey(category_table,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    description=models.CharField(max_length=100)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    size=models.CharField(max_length=10)
    color=models.CharField(max_length=100)
    stock=models.PositiveIntegerField()
    image=models.FileField()
    date=models.DateField(auto_now_add=True)
    rating=models.DecimalField(max_digits=2,decimal_places=1,default=0.0)
    def __str__(self):
        return self.name


    
class cart_table(models.Model):
    USER=models.ForeignKey(user_table,on_delete=models.CASCADE)
    PRODUCT=models.ForeignKey(product_table,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    def total_price(self):
        return self.PRODUCT.price*self.quantity
    def __str__(self):
        return f"{self.USER.name} - {self.PRODUCT.name}"
    
class order_table(models.Model):
    USER=models.ForeignKey(user_table,on_delete=models.CASCADE)
    total_price=models.DecimalField(max_digits=10,decimal_places=2)
    STATUS_CHOICES=[
        ('PENDING','Pending'),
        ('PAID','Paid'),
        ('SHIPPED','Shipped'),
        ('DELIVERED','Delivered'),
        ('CANCELLED','Cancelled')]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    date=models.DateField(auto_now_add=True)
    def __str__(self):
        return f"Order {self.id} by {self.USER.name}"
    
class order_item_table(models.Model):
    ORDER=models.ForeignKey(order_table,on_delete=models.CASCADE)
    PRODUCT=models.ForeignKey(product_table,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    price=models.DecimalField(max_digits=10,decimal_places=2)
    date=models.DateField(auto_now_add=True)
    def __str__(self):
        return f"{self.PRODUCT.name} x {self.quantity}"

class notification_table(models.Model):
    notification=models.CharField(max_length=100)
    date=models.DateField(auto_now_add=True)

class payment_table(models.Model):
    PAYMENT_METHODS=(('COD','Cash On Delivery'),
                    ('RAZORPAY','Razorpay'),
                    ('STRIPE','Stripe'),
                    ('UPI','UPI'))
    PAYMENT_STATUS=(('PENDING','Pending'),
                    ('SUCCESS','Success'),
                    ('FAILED','Failed'),
                    ('REFUNDED','Refunded'))
    USER=models.ForeignKey(user_table,on_delete=models.CASCADE)
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    payment_method=models.CharField(max_length=20,choices=PAYMENT_METHODS)
    payment_id=models.CharField(max_length=200,blank=True,null=True)
    status=models.CharField(max_length=20,choices=PAYMENT_STATUS, default='PENDING')
    date=models.DateTimeField(auto_now_add=True)

class rating_table(models.Model):
    USER=models.ForeignKey(user_table,on_delete=models.CASCADE)
    PRODUCT=models.ForeignKey(product_table,on_delete=models.CASCADE)
    rating=models.CharField(max_length=100)
    review=models.CharField(max_length=100)
    date=models.DateTimeField(auto_now_add=True)
