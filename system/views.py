# Create your views here.
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from MCS.system import forms
from django.http import HttpResponseRedirect, HttpResponse
from MCS.system.models import Shop
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.utils import simplejson

def index(request):
    """ trang chu"""
    form = forms.SignInForm()
    return render_to_response("index.html", {"user":request.user, "form":form}, context_instance=RequestContext(request))

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
            if not "remember" in request.POST:
                request.session.set_expiry(0)
            user = authenticate(username=request.POST["username"], password=request.POST["password"])
            if user.is_active:
                login(request, user)
                res_result = "User authenticated"
            else:
                res_result = "User is blocked"
            response_dict.update({"res_result": res_result})

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
            form = forms.ShopSignUpForm(data=request.POST)
            form.is_valid()
            form.save()
            user = authenticate(username=request.POST["username"], password=request.POST["password"])
            login(request, user)
        
        return HttpResponse(res_data, mimetype="application/json")

    if request.user.is_authenticated():
        return HttpResponseRedirect("/")
    form = forms.ShopSignUpForm()
    return render_to_response("shop_signup.html", {"form": form}, context_instance=RequestContext(request))

def admin(request):
    """ trang cua admin"""
    if not request.user.is_authenticated() or not request.user.is_superuser:
        return HttpResponseRedirect("/")

    if request.is_ajax():
        if "type" not in request.POST:
            return HttpResponse("invalid")

        # multiple status setting
        id_list = request.POST.getlist("for")
        error_list = list()
        if request.POST["type"] == "multi status":
            active_status = True if (request.POST["mode"] == "activate") else False
            for _id in id_list:
                try:
                    user = User.objects.get(id__exact=_id)
                except User.DoesNotExist:
                    error_list.append(_id)
                else:
                    user.is_active = active_status
                    user.save()

            if error_list:
                res_data = simplejson.dumps(error_list)
                return HttpResponse(res_data, mimetype="application/json")
            return HttpResponse()
        if request.POST["type"] == "multi password":
            if not request.user.check_password(request.POST["current_pass"]):
                return HttpResponse("Admin password does not match")
            new_password = request.POST["new_pass"]
            for _id in id_list:
                try:
                    user = User.objects.get(id__exact=_id)
                except User.DoesNotExist:
                    error_list.append(_id)
                else:
                    user.set_password(new_password)
                    user.save()

            if error_list:
                res_data = simplejson.dumps(error_list)
                return HttpResponse(res_data, mimetype="application/json")
            return HttpResponse()

        # single settings
        try:
            user = Shop.objects.get(id__exact=request.POST["id"])
        except Shop.DoesNotExist:
            return HttpResponse("User does not exist")
        else:
            if request.POST["type"] == "single status":
                user.is_active = not user.is_active
                user.save()
                return HttpResponse("User's status has been updated")

            if request.POST["type"] == "single password":
                user.set_password(request.POST["confirm_pass"])
                user.save()
                return HttpResponse()

            # change content
            # critical contents
            if request.POST["content"] == "username":
                try:
                    Shop.objects.get(username__exact=request.POST["new_content"])
                except Shop.DoesNotExist:
                    user.username = request.POST["new_content"]
                    user.save()
                    return HttpResponse()
                else:
                    return HttpResponse("Username existed")
            if request.POST["content"] == "email":
                try:
                    Shop.objects.get(email__exact=request.POST["new_content"])
                except Shop.DoesNotExist:
                    user.email = request.POST["new_content"]
                    user.save()
                    return HttpResponse()
                else:
                    return HttpResponse("Email existed")

            # normal contents
            if request.POST["content"] == "display-name":
                user.display_name = request.POST["new_content"]
            elif request.POST["content"] == "first-name":
                user.first_name = request.POST["new_content"]
            elif request.POST["content"] == "last-name":
                user.last_name = request.POST["new_content"]
            elif request.POST["content"] == "address":
                user.address = request.POST["new_content"]
            elif request.POST["content"] == "phone-number":
                user.phone_number = request.POST["new_content"]
            user.save()
            return HttpResponse()

    response_dict = {}
    response_dict.update({"user": request.user})
    response_dict.update({"shops": Shop.objects.all()})
    response_dict.update({"changeDetailsForm": forms.ChangeDetailsForm()})
    return render_to_response("admin.html", response_dict, context_instance=RequestContext(request))

def usercp(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/")

    response_dict = {"user":request.user}
    changePassForm = forms.ChangeDetailsForm()
    response_dict.update({"changePassForm": changePassForm})
    return render_to_response("usercp.html", response_dict, context_instance=RequestContext(request))

def changepass(request):
    if request.is_ajax():
        user = request.user
        if user.check_password(request.POST["current_pass"]):
            user.set_password(request.POST["confirm_pass"])
            user.save()
            logout(request)
            res_data = simplejson.dumps({})
        else:
            res_current_pass = "Current password does not match"
            response_dict = {"res_current_pass": res_current_pass}
            res_data = simplejson.dumps(response_dict)
        return HttpResponse(res_data, mimetype="application/json")

def success(request):
    return render_to_response("success.html")

def ajax(request):
    if request.is_ajax():
        print request.POST
        return HttpResponse("response")

    print request.POST
#        res_username = ""
#        res_password = ""
#        if request.POST["username"] != "" and request.POST["password"] != "":
#            user = User()
#            try:
#                user = User.objects.get(username__exact=request.POST["username"])
#            except User.DoesNotExist:
#                res_username = "Username does not exist"
#
#            if not user.check_password(request.POST["password"]):
#                res_password = "Password does not match"
#
#        response_dict = {"res_username": res_username, "res_password": res_password}
#        res_data = simplejson.dumps(response_dict)
#        return HttpResponse(res_data, mimetype="application/json")

    return render_to_response("ajax.html", {"shops": forms.Shop.objects.all()})

def search(request):
    if request.is_ajax():
        print request.GET
        searchValue = request.GET["globalSearch"]
        if searchValue == "Enter your search" or searchValue == "":
            return HttpResponse()
        return HttpResponse("response")