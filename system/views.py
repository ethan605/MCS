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
    return render_to_response("index.html", {"user": request.user})

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

#    if request.method == "POST":
#        print request.POST
#        form = SignInForm(data=request.POST)
#        if form.is_valid():
#            username = form.cleaned_data["username"]
#            password = form.cleaned_data["password"]
#            if not form.cleaned_data["remember"]:
#                request.session.set_expiry(0)
#            user = authenticate(username=username, password=password)
#            if user is not None:
#                if user.is_active:
#                    login(request,user)
#                    return HttpResponseRedirect("/")
#                else:
#                    message = user.username + " is blocked"
#                    return render_to_response("failure.html", {"message":message})

    form = SignInForm()
    return render_to_response("sign_in.html", {"form": form}, context_instance=RequestContext(request))

def sign_out(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/")
    
    logout(request)
    return render_to_response("sign_out.html")

def signup(request):
    """ cua hang dang ki"""
    if request.is_ajax():
        print request.POST
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
            print request.POST
            form = ShopSignUpForm(data=request.POST)
            form.is_valid()
            form.save()
            user = authenticate(username=request.POST["username"], password=request.POST["password"])
            login(request, user)
        return HttpResponse(res_data, mimetype="application/json")

    if request.method == "POST":
        print request.POST

#    if request.method == "POST":
#        form = ShopSignUpForm(data=request.POST)
#        if form.is_valid():
#            form.save()
#            username = form.cleaned_data["username"]
#            password = form.cleaned_data["password"]
#            user = authenticate(username=username, password=password)
#            login(request, user)
#            return render_to_response("success.html")

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
    render_to_response("success.html")

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
        print res_data
        return HttpResponse(res_data, mimetype="application/json")

    return render_to_response("ajax.html")