# Create your views here.
from django.shortcuts import render_to_response
from MCS.system.forms import SignInForm, ShopSignUpForm
from django.http import HttpResponseRedirect
from MCS.system.models import Shop
from django.contrib.auth import authenticate, login, logout

def index(request):
    """ trang chu"""
    if not request.user.is_authenticated():
        return render_to_response("index.html")

    return render_to_response("index.html", {"username": request.user.username})

def sign_in(request):
    """ trang dang nhap"""
    if request.user.is_authenticated():
        return HttpResponseRedirect("/usercp/")
    
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
        form = SignInForm()
    return render_to_response("sign_in.html",{"form": form})

def signout(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/")
    
    logout(request)
    return render_to_response("sign_out.html")

def shop_signup(request):
    """ cua hang dang ki"""

    if request.method == "POST":
        form = ShopSignUpForm(data=request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            login(request, user)
            return render_to_response("success.html")
    else:
        if request.user.is_authenticated():
            return HttpResponseRedirect("/")
        form = ShopSignUpForm()
    return render_to_response("shop_signup.html",{"form": form})

def admin(request):
    """ trang cua admin"""
    if not request.user.is_authenticated() and request.user.is_superuser:
        message = "user is not admin"
        return render_to_response("failure.html",{"message": message})
    shops = Shop.objects.all()
    return render_to_response("admin.html", {"shops": shops})

def usercp(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/signin/")

    return render_to_response("usercp.html", {"username": request.user.username})
