"""
Created on Nov 27, 2011

@author: THANG
"""
from django import forms
from MCS.system.models import Shop

class ChangePassForm(forms.Form):
    current_pass = forms.CharField(widget=forms.PasswordInput)
    new_pass = forms.CharField(widget=forms.PasswordInput)
    confirm_pass = forms.CharField(widget=forms.PasswordInput)

class SignInForm(forms.Form):
    """ form dang nhap tu link localhost:8000/signin/"""
    
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    remember = forms.BooleanField(required=False)
        
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
