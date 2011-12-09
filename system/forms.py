"""
Created on Nov 27, 2011

@author: THANG
"""
from django import forms
from MCS.system.models import User, Shop

class SignInForm(forms.Form):
    """ form dang nhap tu link localhost:8000/signin/"""
    
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    remember = forms.BooleanField(required=False)

#    def clean_username(self):
#        try:
#            User.objects.get(username__exact = self.cleaned_data["username"])
#        except User.DoesNotExist:
#            raise forms.ValidationError("Username does not exist")
#        return self.cleaned_data["username"]
#
#    def clean_password(self):
#        if "username" in self.cleaned_data:
#            user = User.objects.get(username__exact = self.cleaned_data["username"])
#            if not user.check_password(self.cleaned_data["password"]):
#                raise forms.ValidationError("Password does not match")
#        return self.cleaned_data["password"]
        
class ShopSignUpForm(forms.Form):
    """ form dang ky nhung thong tin co ban cua cua hang
    link: localhost:8000/shop/signup/"""
    
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    re_password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()
    re_email = forms.EmailField()
    display_name = forms.CharField()
    address = forms.CharField()
    phone_number = forms.IntegerField()

#    def clean_username(self):
#        try:
#            Shop.objects.get(username = self.cleaned_data["username"])
#        except Shop.DoesNotExist:
#            return self.cleaned_data["username"]
#        raise forms.ValidationError("User name has used")
        
#    def clean_password(self):
#        if "password" in self.cleaned_data:
#            if len(self.cleaned_data["password"]) < 6:
#                raise forms.ValidationError("Password is to short")
#            else:
#                return self.cleaned_data["password"]
        
#    def clean_re_password(self):
#        if "password" in self.cleaned_data  and "re_password" in self.cleaned_data:
#            if self.cleaned_data["password"] != self.cleaned_data["re_password"]:
#                raise forms.ValidationError("Password is not match")
#            else:
#                return self.cleaned_data["re_password"]
        
#    def clean_email(self):
#        return self.cleaned_data["email"]
#
#    def clean_re_email(self):
#        if "email" in self.cleaned_data and "re_email" in self.cleaned_data:
#            if self.cleaned_data["email"] != self.cleaned_data["re_email"]:
#                raise forms.ValidationError("Email is not match")
#            return self.cleaned_data["re_email"]

    def save(self):
        new_user = Shop()
        new_user.display_name = self.cleaned_data["display_name"]
        new_user.username = self.cleaned_data["username"]
        new_user.set_password(self.cleaned_data["password"])
        new_user.email = self.cleaned_data["email"]
        new_user.address = self.cleaned_data["address"]
        new_user.phone_number = self.cleaned_data["phone_number"]
        new_user.save()
        return new_user
