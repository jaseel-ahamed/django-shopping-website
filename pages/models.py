from django.db import models

# Create your models here.
class Contact(models.Model):
    contact_name=models.CharField(max_length=255)
    contact_email=models.EmailField(max_length=255)
    subject=models.CharField(max_length=255)
    contact_message=models.TextField()

    def __str__(self):
        return self.contact_name

class Registration(models.Model):
    register_name=models.CharField(max_length=255)
    register_email=models.EmailField(max_length=255)
    register_number=models.CharField(max_length=255)
    register_user=models.CharField(max_length=255)
    register_propic=models.FileField(null=True)
    password=models.CharField(max_length=255)

    def __str__(self):
        return self.register_name

class Product(models.Model): #uploaded product details are shown in this model
    product_name=models.CharField(max_length=255)
    product_price=models.FloatField()
    product_image=models.CharField(max_length=255)
    product_desc=models.CharField(null=True,max_length=400)
    product_cat=models.IntegerField(null=True)
    def __str__(self):
        return self.product_name

class Cart(models.Model):
    username=models.CharField(max_length=255)
    cart_id=models.IntegerField()
    cart_name=models.CharField(max_length=255)
    cart_image=models.CharField(null=True,max_length=255)
    cart_desc=models.TextField(null=True)
    cart_price=models.FloatField()
    cart_quantity=models.IntegerField()
    total_price=models.FloatField(default=0)

    def __str__(self):
        return self.cart_name
    
class Category(models.Model):
    cat_name=models.CharField(max_length=255)
    cat_image=models.ImageField(null=True,upload_to='uploads')
    cat_pro_count=models.IntegerField()

    def __str__(self): 
        return self.cat_name


class Order(models.Model):
    prod_name=models.CharField(max_length=255)
    prod_image=models.CharField(null=True,max_length=255)
    prod_qty=models.IntegerField()
    prod_price=models.FloatField()
    prod_tot=models.FloatField(default=0)
    cust_user=models.CharField(max_length=255)
    deliv_address=models.TextField()
    deliv_type=models.CharField(max_length=255,default='cod')
    order_status=models.IntegerField(default=0)
    deliv_status=models.IntegerField(default=0)
    
    def __str__(self):
        return self.prod_name

class Wishlist(models.Model):
    username=models.CharField(max_length=255,null=True)
    prod_name=models.CharField(max_length=255)
    prod_image=models.CharField(null=True,max_length=255)
    prod_price=models.FloatField()
    prod_desc=models.CharField(null=True,max_length=400)

    def __str__(self):
        return self.prod_name
