#coding=utf-8
#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
# from captcha.fields import CaptchaField
from .models import MyUser
from captcha.fields import CaptchaField

#注册表
class RegisterForm(forms.Form):
    # username = forms.CharField(
    #     widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '用户名'}),
    #     error_messages={'required': '请输入用户名'})
    # email = forms.EmailField(
    #     widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '邮箱地址'}),
    #     error_messages={'required': '请输入邮箱地址', 'invalid': '请输入正确的邮箱地址'})
    # password1 = forms.CharField(
    #     widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入5位以上密码'}),
    #     error_messages={'required': '请输入密码'})
    # password2 = forms.CharField(
    #     widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请再次输入密码'}),
    #     error_messages={'required': '请再次输入密码'})
    captcha = CaptchaField(error_messages={'required': '请输入验证码!','invalid':'验证码错误!'})
    # captcha = CaptchaField(label='请输入下方验证码',)
    #验证用户名有效性
    # def clean_username(self):
    #     username = self.cleaned_data.get("username")
    #     print "test,..."
    #     #验证用户名是否已经被注册
    #     try:
    #         exists = MyUser.objects.get(username=username)
    #         raise forms.ValidationError("该用户名已被注册")
    #     except MyUser.DoesNotExist:
    #         return username
    #     #验证用户名是否正常
    #     except:
    #         print "raise"
    #         raise 

    # #验证密码有效性
    # def clean_password1(self):
    #     # Check that the two password entries match
    #     password1 = self.cleaned_data.get("password1")
    #     print password1
    #     print "test1"
    #     #验证密码长度是否大于4
    #     if len(password1) <= 4:
    #         raise forms.ValidationError("密码太短，应超过5位！")

    #验证密码有效性
    # def clean_password2(self):
    #     # Check that the two password entries match
    #     password1 = self.cleaned_data.get("password1")
    #     if len(password1) <= 4:
    #         raise forms.ValidationError("密码太短，应超过5位！")
    #     #验证密码长度是否大于4
    #     # if len(password1) <= 4:
    #     #     raise forms.ValidationError("密码太短，应超过5位！")
    #     #验证两次输入的密码是否相同
    #     password2 = self.cleaned_data.get("password2")
    #     print "test2"
    #     print password1
    #     print password2
    #     if password1 != password2:
    #         raise forms.ValidationError("两次输入密码不相同，请核对!")
    #     return password2



#登录表
class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '用户名'}),
        error_messages={'required': '请输入用户名'})
    password = forms.CharField(
        widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': '密码'}),
        error_messages={'required': '请输入密码'})
    captcha = CaptchaField(error_messages={'required': '请输入验证码','invalid':'验证码错误' })
    def clean_username(self):
        username = self.cleaned_data.get("username")
        try:
            exists = MyUser.objects.get(username=username)
            print exists
            return username
        except MyUser.DoesNotExist:
            raise forms.ValidationError("用户不存在！")


#登录表
class RepasswordForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '用户名'}),
        error_messages={'required': '请输入用户名'})
    phonenumber = forms.CharField(
        widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '常用手机号'}),
        error_messages={'required': '请输入常用手机号'})
    captcha = CaptchaField(error_messages={'required': '请输入验证码','invalid':'验证码错误' })
    def clean_username(self):
        username = self.cleaned_data.get("username")
        try:
            exists = MyUser.objects.get(username=username)
            return username
        except MyUser.DoesNotExist:
            raise forms.ValidationError("用户不存在！")


#在admin中增加用户
class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('email', 'username')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

#在admin中更改用户信息
class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ('email', 'password', 'username')

    def clean_password(self):
        return self.initial["password"]
