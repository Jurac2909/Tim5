from django.shortcuts import render
from urllib import request
from django.http import HttpResponse
from django.views import View
from . models import Product, Customer
from django.db.models import Count
from . forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages

# Create your views here.

def home(request): 
    return render(request, "app/home.html")

class CategoryView(View):
    def get(self, request, val):
        product = Product.objects.filter(category=val) 
        title = Product.objects.filter(category=val).values('title')
        return render(request, "app/category.html", locals())

class CategoryTitle(View):
    def get(self,request,val):
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        return render(request,"app/category.html",locals())
    
class ProductDetail(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk) 
        return render(request,"app/productdetail.html",locals())

class CustomerRegistration(View):
    def get(self,request):
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