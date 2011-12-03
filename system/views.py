# Create your views here.
from django.shortcuts import render_to_response
from MCS.system.forms import SignInForm, ShopSignUpForm
from django.http import HttpResponseRedirect
from models import User
from MCS.system.models import Shop

def home(request):
    """ trang chu"""
    
    return render_to_response('index.html')

def sign_in(request):
    """ trang dang nhap
        user: admin; pass: admin"""
    
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            user = User.objects.get(username = form.cleaned_data['username'])
            if user.priority == 1:
                return HttpResponseRedirect('/admin/')
            else:
                return HttpResponseRedirect('/usercp/')
        else: 
            return HttpResponseRedirect('/failure/')
    else:
        form = SignInForm()
    return render_to_response('sign_in.html',{'form': form})

def shop_signup(request):
    """ cua hang dang ki"""
    
    if request.method == 'POST':
        form = ShopSignUpForm(data=request.POST)
        if form.is_valid():
            print form.clean_username()
            form.save()
            return render_to_response('success.html')
    else:
        form = ShopSignUpForm()
    return render_to_response('shop_signup.html',{'form': form})

def admin(request):
    """ trang cua admin"""
    
    shops = Shop.objects.all()
    return render_to_response('admin.html',{'shops': shops})

def usercp(request):
    """ user control panel site"""
    return render_to_response('usercp.html')

def success(request):
    """ thong bao dang nhap thanh cong"""
    
    return render_to_response('success.html')

def failure(request):
    """ thong bao dang nhap that bai"""
    
    return render_to_response('failure.html')