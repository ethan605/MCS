# Create your views here.
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from MCS.system.forms import SignInForm, ShopSignUpForm
from django.http import HttpResponseRedirect, HttpResponse
from MCS.system.models import Shop
from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions.backends.base import SessionBase
from django.template import RequestContext

def index(request):
    """ trang chu"""
    return render_to_response("index.html", {"user": request.user})

def sign_in(request):
    """ trang dang nhap"""
    
    if request.user.is_authenticated():
        return HttpResponseRedirect("/usercp/")
    
    if request.method == "POST":
        form = SignInForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            checkbox = form.cleaned_data["remember"]
            if checkbox == False:
                request.session.set_expiry(0)
            user = authenticate(username = username, password = password)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return HttpResponseRedirect("/usercp/")
                else:
                    message = user.username + " is blocked"
                    return render_to_response("failure.html", {"message":message})
    else:
        form = SignInForm()
    return render_to_response("sign_in.html", {"form": form}, context_instance=RequestContext(request))

def sign_out(request):
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
    return render_to_response("shop_signup.html", {"form": form}, context_instance=RequestContext(request))

def admin(request):
    """ trang cua admin"""
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/signin/")
    else:
        if request.user.is_superuser:
            shops = Shop.objects.all()
            return render_to_response("admin.html", {"shops": shops})
        else:
            return HttpResponseRedirect("/usercp/")
    if not request.user.is_authenticated() or not request.user.is_superuser:
        return HttpResponseRedirect("/")
    shops = Shop.objects.all()
    return render_to_response("admin.html", {"user":request.user, "shops":shops})

def usercp(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/signin/")

    return render_to_response("usercp.html", {"user": request.user})

def ajax(request):
    if request.is_ajax():
        user = User()
        try:
            user = User.objects.get(username__exact=request.POST["username"])
        except User.DoesNotExist:
            if not "password" in request.POST:
                return HttpResponse("Username does not exist")
            return HttpResponse()

        if not "password" in request.POST:
            return HttpResponse("validated")
        if request.POST["password"] == "":
            return HttpResponse("This field is required")
        if not user.check_password(request.POST["password"]):
            return HttpResponse("Password does not match")
        return HttpResponse("validated")

    return render_to_response("ajax.html")
