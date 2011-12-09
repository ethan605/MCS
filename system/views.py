# Create your views here.
import email
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from MCS.system.forms import SignInForm, ShopSignUpForm
from django.http import HttpResponseRedirect, HttpResponse
from MCS.system.models import Shop
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.utils import simplejson

def index(request):
    """ trang chu"""
    form = SignInForm()
    return render_to_response("index.html", {"user":request.user, "form":form}, context_instance=RequestContext(request))
#    return render_to_response("index.html", {"user": request.user})

def sign_in(request):
    """ trang dang nhap"""
    if request.user.is_authenticated():
        return HttpResponseRedirect("/usercp/")

    if request.is_ajax():
        res_username = ""
        res_password = ""
        try:
            user = User.objects.get(username__exact=request.POST["username"])
        except User.DoesNotExist:
            res_username = "Username does not exist"
        else:
            if not user.check_password(request.POST["password"]):
                res_password = "Password does not match"

        response_dict = {"res_username": res_username, "res_password": res_password}

        if res_username == "" and res_password == "":
            if "remember" in request.POST and not request.POST["remember"]:
                request.session.set_expiry(0)
            user = authenticate(username=request.POST["username"], password=request.POST["password"])
            if user.is_active:
                login(request, user)
            else:
                response_dict.update({"res_blocked": "User is blocked"})

        res_data = simplejson.dumps(response_dict)
        return HttpResponse(res_data, mimetype="application/json")

    form = SignInForm()
    return render_to_response("sign_in.html", {"form": form}, context_instance=RequestContext(request))

def sign_out(request):
    if request.is_ajax():
        logout(request)
        return HttpResponse()

def signup(request):
    """ cua hang dang ki"""
    if request.is_ajax():
        try:
            User.objects.get(username__exact=request.POST["username"])
        except User.DoesNotExist:
            res_username = ""
        else:
            res_username = "Username existed"

        try:
            User.objects.get(email__exact=request.POST["email"])
        except User.DoesNotExist:
            res_email = ""
        else:
            res_email = "Email registered"

        response_dict = {"res_username": res_username, "res_email": res_email}
        res_data = simplejson.dumps(response_dict)

        if res_username == "" and res_email == "":
            form = ShopSignUpForm(data=request.POST)
            form.is_valid()
            form.save()
            user = authenticate(username=request.POST["username"], password=request.POST["password"])
            login(request, user)
        
        return HttpResponse(res_data, mimetype="application/json")

    if request.user.is_authenticated():
        return HttpResponseRedirect("/")
    form = ShopSignUpForm()
    return render_to_response("shop_signup.html", {"form": form}, context_instance=RequestContext(request))

def admin(request):
    """ trang cua admin"""
    if not request.user.is_authenticated() or not request.user.is_superuser:
        return HttpResponseRedirect("/")
    shops = Shop.objects.all()
    return render_to_response("admin.html", {"user":request.user, "shops":shops})

def usercp(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/signin/")

    return render_to_response("usercp.html", {"user": request.user})

def success(request):
    return render_to_response("success.html")

def ajax(request):
    if request.is_ajax():
        res_username = ""
        res_password = ""
        if request.POST["username"] != "" and request.POST["password"] != "":
            user = User()
            try:
                user = User.objects.get(username__exact=request.POST["username"])
            except User.DoesNotExist:
                res_username = "Username does not exist"

            if not user.check_password(request.POST["password"]):
                res_password = "Password does not match"

        response_dict = {"res_username": res_username, "res_password": res_password}
        res_data = simplejson.dumps(response_dict)
        return HttpResponse(res_data, mimetype="application/json")

    return render_to_response("ajax.html")