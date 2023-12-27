
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from . models import Contact
from . models import Registration
from . functions import handle_uploaded_file
from .forms import AddProductForm
from .models import Product
from .models import Cart
from .models import Category
from .models import Order
from .models import Wishlist
from django.contrib import messages
from django.db.models import Q


# Create your views here.
def index(request):
    if request.method=='POST':
        c_name=request.POST['contact_name']
        c_email=request.POST['contact_email']
        sub=request.POST['subject']
        c_msg=request.POST['contact_message']
        contact=Contact(contact_name=c_name,contact_email=c_email,subject=sub,contact_message=c_msg)
        contact.save()

    if 'sm' in request.GET:
        products = Product.objects.all().order_by('-id')
    else:
        products = Product.objects.all().order_by('-id')[:4]

    category = Category.objects.all().values()
    context = {
        'products' : products,
        'category' : category,
    }
    template=loader.get_template("index.html")
    return HttpResponse(template.render(context,request))

def registration(request):
    msg=""
    if request.method=='POST':
        reg_name=request.POST['register_name']
        reg_email=request.POST['register_email']
        reg_number=request.POST['register_number']
        reg_propic=request.FILES['register_propic'].name
        reg_user=request.POST['register_user']
        reg_pass=request.POST['password']

        #regexist=Registration(Q(register_email=reg_email) |Q(register_number=reg_number) | Q(register_user=reg_user))

        userexist=Registration.objects.filter(register_user=reg_user)
        emailexist=Registration.objects.filter(register_email=reg_email)
        numexist=Registration.objects.filter(register_number=reg_number)

        if emailexist:
            msg="Email already exist"
        elif numexist:
            msg="Number already exist"
        elif userexist:
            msg="Username already exist"
        else:
            reg=Registration(register_name=reg_name,register_email=reg_email,register_number=reg_number,register_user=reg_user,password=reg_pass,register_propic=reg_propic)
            reg.save()
            handle_uploaded_file(request.FILES['register_propic']) 
            return HttpResponseRedirect("login")
    context={
        'msg': msg
    }
    template = loader.get_template('registration.html')
    return HttpResponse(template.render(context,request))

def login(request):
    if 'usersess' in request.session:
        return HttpResponseRedirect("account")
    if request.method=='POST':
        username=request.POST['user']
        password=request.POST['pass']
        login=Registration.objects.filter(register_user=username,password=password).values()
        if(login):
            request.session['usersess']=username
            return HttpResponseRedirect("account")
    template=loader.get_template("login.html")
    return HttpResponse(template.render({},request))

def adminlogin(request):
    if 'adminsess' in request.session:
        return HttpResponseRedirect("adminproducts")
    if request.method=='POST':
        username=request.POST['user']
        password=request.POST['pass']
        if username=='aish' and password=='123456':
            request.session['adminsess']=username
            return HttpResponseRedirect("adminproducts")
        else:
            return HttpResponseRedirect("adminlogin?inv=1")
    template=loader.get_template("adminlogin.html")
    return HttpResponse(template.render({},request))

def adminproducts(request):
    if 'adminsess' not in request.session:
        return HttpResponseRedirect("adminlogin")
    else:
        adminuser = request.session['adminsess']

        # get all products
        products = Product.objects.all().order_by('-id').values()
        cats = Category.objects.all()

           
        #create context for pass to template
        context = {
            'products' : products,
            'cats' : cats
        } 
        template=loader.get_template("adminproducts.html")
        return HttpResponse(template.render(context,request))

def admineditprod(request,id):
    if request.method=='POST':
            id=request.POST['id']
            product_name=request.POST['product_name']
            product_price=request.POST['product_price']
            product_cat=request.POST['product_cat']
            prod = Product.objects.filter(id=id)[0]
            prod.product_name=product_name
            prod.product_price=product_price
            prod.product_cat=product_cat

            if len(request.FILES) != 0:
                product_image=request.FILES['product_image']
                prod.product_image=product_image
                handle_uploaded_file(request.FILES['product_image'])
            prod.save()
             
            messages.add_message(request, messages.SUCCESS, 'Product uploaded successfully')
            return HttpResponseRedirect("/adminproducts")  
        
    product=Product.objects.filter(id=id)[0]
    cat=Category.objects.all()
    context={
        'product': product,
        'cat':cat
    }
    template=loader.get_template("admineditprod.html")
    return HttpResponse(template.render(context,request))



def admindelprod(request,id):
    product=Product.objects.filter(id=id)[0]
    product.delete()
    return HttpResponseRedirect('/adminproducts')


def adminlogout(request):
    del request.session["adminsess"]
    return HttpResponseRedirect("adminlogin")



def account(request):
    if 'usersess' not in request.session:
        return HttpResponseRedirect("login")
    profile=Registration.objects.filter(register_user=request.session['usersess'])
    context = {
        'profile':profile,
    }
    template=loader.get_template("account.html")
    return HttpResponse(template.render(context,request))
    # or give like this --return render(request,'account.html',{'profile' : profile})


def logout(request):
    del request.session["usersess"]
    return HttpResponseRedirect("login")

def addproduct(request):
    if request.method=='POST':
        addproductform=AddProductForm(request.POST,request.FILES)
        if addproductform.is_valid():
            product_name=request.POST['product_name']
            product_price=request.POST['product_price']
            product_image=request.FILES['product_image'].name
            product_desc=request.POST['product_desc']
            product_cat=request.POST['product_cat']
            addproduct = Product(product_name=product_name,product_price=product_price,product_desc=product_desc,product_image=product_image,product_cat=product_cat)
            addproduct.save()
            handle_uploaded_file(request.FILES['product_image']) 
            messages.add_message(request, messages.SUCCESS, 'Product uploaded successfully')
            return HttpResponseRedirect("products/0")  
    else:  
        addproductform = AddProductForm()  
    template = loader.get_template('addproduct.html')
    return HttpResponse(template.render({'form':addproductform},request))



def viewproducts(request,id):
    cats = Category.objects.all()
    # if id is 0 it shows all products

    if id==0:
        products = Product.objects.all().order_by('-id').values()
    else:
        products = Product.objects.filter(product_cat=id).order_by('-id').values()
    context = {
        'products' : products,
        'cats' : cats 
    }
    template = loader.get_template('viewproducts.html')
    return HttpResponse(template.render(context,request))


def addtocart(request,id):
    if 'usersess' in request.session:
        username = request.session['usersess']
        prod=Cart.objects.filter(username=username, cart_id=id).values()
        if prod:
            cart=Cart.objects.filter(username=username, cart_id=id)[0]
            cart.cart_quantity+=1
            cart.save()
        else:
            x = Product.objects.filter(id=id)[0]
            cart=Cart(username=username,cart_id=x.id,cart_name=x.product_name,cart_price=x.product_price,cart_quantity=1,cart_image=x.product_image,cart_desc=x.product_desc,total_price=x.product_price)
            cart.save()
        
        return HttpResponseRedirect('/cart')
    
    else:
        return HttpResponseRedirect('/login')
    

def cart(request):
    if 'usersess' not in request.session:
        return HttpResponseRedirect('/login')
    else:
        username = request.session['usersess']

        # Update and save qty and tot price
        if request.method=='POST':
            qty=int(request.POST['qty'])
            cid=request.POST['cid']
            chg=request.POST['chg']
            if chg=='inc':
                qty+=1
            elif chg=='dec':
                if qty>1:
                    qty-=1
            
            cart=Cart.objects.filter(id=cid)[0]
            cart.cart_quantity=qty
            cart.total_price=qty * cart.cart_price
            cart.save() 


        # get all cart values
        cart = Cart.objects.filter(username=username).order_by('-id').values()


        # get total price
        cart2 = Cart.objects.filter(username=username)
        gtot=0
        for x in cart2:
            gtot=gtot+x.total_price
            
        #create context for pass to template
        context = {
            'cart' : cart,
            'gtot' : gtot
        } 
        template=loader.get_template("cart.html")
        return HttpResponse(template.render(context,request))

def delcart(request,id):
    cart=Cart.objects.filter(id=id)[0]
    cart.delete()
    return HttpResponseRedirect('/cart')


def checkout(request):
    if 'usersess' not in request.session:
        return HttpResponseRedirect('/login')
    else:
        username = request.session['usersess']

    if request.method=='POST':
        if 'deliv_address' in request.POST:
            order=Order.objects.filter(cust_user=username)
            for x in order:
                x.deliv_address=request.POST['deliv_address']
                x.deliv_type=request.POST['deliv_type']
                x.save()
            
        else:
            crt=Cart.objects.filter(username = username)
            for x in crt:
                ordr=Order(
                    prod_name=x.cart_name, 
                    prod_image=x.cart_image, 
                    prod_qty=x.cart_quantity,
                    prod_price=x.cart_price,
                    prod_tot=x.total_price,
                    cust_user=x.username,
                )
                ordr.save()
        return HttpResponseRedirect('/checkout')
    
    
    order=Order.objects.filter(cust_user = username)
    gtot=0
    for x in order:
        gtot = gtot + x.prod_tot * x.prod_qty

    context = {
        'order' : order,
        'gtot' : gtot,
    }

    template=loader.get_template("checkout.html")
    return HttpResponse(template.render(context,request))


def delorder(request,id):
    order=Order.objects.filter(id=id)[0]
    order.delete()
    return HttpResponseRedirect('/checkout')


def orders(request):
    if 'usersess' not in request.session:
        return HttpResponseRedirect('/login')
    else:
        username = request.session['usersess']

    order=Order.objects.filter(cust_user = username)

    gtot=0
    for x in order:
        gtot = gtot + x.prod_tot * x.prod_qty
        adrs = x.deliv_address
        dtyp = x.deliv_type

    context = {
        'order' : order,
        'gtot' : gtot,
        'adrs' : adrs,
        'dtyp' : dtyp,
    }
 
    template=loader.get_template("orders.html")
    return HttpResponse(template.render(context,request))


    
def orderplaced(request):
    if 'usersess' not in request.session:
        return HttpResponseRedirect('/login')
    else:
        username = request.session['usersess']

    if request.method=='POST':
        if 'order_status' in request.POST:
            ordr=Order.objects.filter(cust_user = username)
            for x in ordr:
                x.order_status=1
                x.save()
                
    template=loader.get_template("orderplaced.html")
    return HttpResponse(template.render({},request))


def purchase(request):
    if 'usersess' not in request.session:
        return HttpResponseRedirect('/login')
    else:
        username = request.session['usersess']

        order=Order.objects.filter(cust_user = username)

    gtot=0
    for x in order:
        gtot = gtot + x.prod_tot * x.prod_qty
        adrs = x.deliv_address
        dtyp = x.deliv_type

    context = {
        'order' : order,
        'gtot' : gtot,
        'adrs' : adrs,
        'dtyp' : dtyp,
    }
                
    template=loader.get_template("purchase.html")
    return HttpResponse(template.render(context,request))

def addtowish(request,id):
    if 'usersess' not in request.session:
        return HttpResponseRedirect('/login')
       
    else:   
        username = request.session['usersess']
        wish=Product.objects.filter(id=id)[0]
        wishlist=Wishlist(
            username=username,
            prod_name=wish.product_name, 
            prod_price=wish.product_price,
            prod_image=wish.product_image, 
            prod_desc=wish.product_desc,
            )
        wishlist.save()
       
    return HttpResponseRedirect('/wishlist')

def wishlist(request):
    if 'usersess' not in request.session:
        return HttpResponseRedirect("/login")
    else:
        username = request.session['usersess']  

    wish=Wishlist.objects.filter(username=username)

    context = {
    'wish' : wish
    }
    
    template=loader.get_template("wishlist.html")
    return HttpResponse(template.render(context,request))

def delwish(request,id):
    wish=Wishlist.objects.filter(id=id)[0]
    wish.delete()
    return HttpResponseRedirect('/wishlist')

def search(request):
    search=request.GET['search']
    search=Product.objects.filter(product_name__contains=search)
    context = {
        'search' : search,
    }
    template=loader.get_template("search.html")
    return HttpResponse(template.render(context,request))