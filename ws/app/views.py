from django.shortcuts import render, redirect
from urllib import request
from django.http import JsonResponse
from django.views import View
from . models import Product, Customer, Cart
from django.db.models import Q
from . forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages

# Create your views here.

def home(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user)) 
    return render(request, "app/home.html", locals())

class CategoryView(View):
    def get(self, request, val):
        totalitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user)) 
        product = Product.objects.filter(category=val) 
        title = Product.objects.filter(category=val).values('title')
        return render(request, "app/category.html", locals())

class CategoryTitle(View):
    def get(self,request,val):
        totalitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user)) 
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        return render(request,"app/category.html",locals())
    
class ProductDetail(View):
    def get(self,request,pk):
        totalitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user)) 
        product = Product.objects.get(pk=pk) 
        return render(request,"app/productdetail.html",locals())

class CustomerRegistration(View):
    def get(self,request):
        totalitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user)) 
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', locals())
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"User Registered Successfully")
        else:
            messages.warning(request, "invalid Input Data")
        return render(request, 'app/customerregistration.html', locals())

class ProfileView(View):
    def get(self,request):
        totalitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user)) 
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', locals())
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            country = form.cleaned_data['country']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            zipcode = form.cleaned_data['zipcode']

            reg  = Customer(user=user, name=name, country=country, mobile=mobile, city=city, zipcode=zipcode)
            reg.save()
            messages.success(request, "Profile Saved Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request, 'app/profile.html', locals())


def address(request):
    add = Customer.objects.filter(user=request.user)
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user)) 
    return render(request, 'app/address.html', locals())

class updateAddress(View):
    def get(self,request,pk):
        totalitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user)) 
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request, 'app/updateAddress.html',locals())
    def post(self,request,pk):
        form =  CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.country = form.cleaned_data['country']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request, "Profile Updated Successfully")
        else:
            messages.warning(request,"invalid Input Data")
        return render(request, 'app/updateAddress.html', locals())
    
def add_to_cart(request):
    user=request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect("/cart")

def show_cart(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user)) 
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.selling_price
        amount = amount + value
    totalamount = amount + 2
    return render(request, 'app/addtocart.html', locals())


def plus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        totalamount=0
        for p in cart:
            value = p.quantity * p.product.selling_price
            amount = amount + value
        totalamount = amount + 2
        print(prod_id)
        data ={
            'quantity' : c.quantity,
            'amount' : amount,
            'totalamount:':totalamount
        }
        return JsonResponse(data)


def minus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        totalamount=0
        for p in cart:
            value = p.quantity * p.product.selling_price
            amount = amount + value
        totalamount = amount + 2
        print(prod_id)
        data ={
            'quantity' : c.quantity,
            'amount' : amount,
            'totalamount:':totalamount
        }
        return JsonResponse(data)
    
def remove_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        totalamount=0
        for p in cart:
            value = p.quantity * p.product.selling_price
            amount = amount + value
        totalamount = amount + 2
        print(prod_id)
        data ={
            'amount' : amount,
            'totalamount:':totalamount
        }
        return JsonResponse(data)
    
class checkout(View):
    def get(self,request):
        totalitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user)) 
        user=request.user
        add=Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        amount = 0
        for p in cart_items:
            value = p.quantity * p.product.selling_price
            amount = amount + value
        totalamount = amount + 2
        return render(request, 'app/checkout.html', locals())
    
    