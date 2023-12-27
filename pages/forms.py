from django import forms
from . models import Category

class AddProductForm(forms.Form):
    product_name=forms.CharField(max_length=255,label="Enter product name")
    product_price=forms.FloatField(label="Enter product price")
    product_desc=forms.CharField(max_length=400,label="Enter product description")
    product_image=forms.FileField(label="Choose product image")
    cat=Category.objects.all()
    catlist = []
    for x in cat:
        catlist.append((x.id, x.cat_name))
    CHOICES = tuple(catlist)
    product_cat = forms.ChoiceField(choices=CHOICES,label="Choose category")
