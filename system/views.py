# Create your views here.
from django.shortcuts import render_to_response
from MCS.system.forms import SignInForm, ShopSignUpForm
from django.http import HttpResponseRedirect
from models import User
from MCS.system.models import Shop
from django.contrib.auth import authenticate, login

def index(request):
    """ trang chu"""
    return render_to_response("index.html")

def sign_in(request):
    """ trang dang nhap
        user: admin; pass: admin"""
    if request.method == "POST":
        form = SignInForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username = username, password = password)
            print user
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return HttpResponseRedirect("/usercp/")
                else:
                    message = user.username + " is blocked"
                    return render_to_response("failure.html", {"message":message})
            else:
                message = "invalid login"
                return render_to_response("failure.html", {"message":message})
    else:
        form = SignInForm()
    return render_to_response("sign_in.html",{"form": form})

def shop_signup(request):
    """ cua hang dang ki"""
    if request.method == "POST":
        form = ShopSignUpForm(data=request.POST)
        if form.is_valid():
            print form.clean_username()
            form.save()
            return render_to_response("success.html")
    else:
        form = ShopSignUpForm()
    return render_to_response("shop_signup.html",{"form": form})

def admin(request):
    """ trang cua admin"""
    if not request.user.is_authenticated():
        
        message = "user is not admin"
        return render_to_response("failure.html",{"message": message})
    shops = Shop.objects.all()
    return render_to_response("admin.html", {"shops": shops})

def usercp(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/signin/")
    """ user control panel site"""
    print request.user
    return render_to_response("usercp.html")

def success(request):
    """ thong bao dang nhap thanh cong"""
    return render_to_response("success.html")
