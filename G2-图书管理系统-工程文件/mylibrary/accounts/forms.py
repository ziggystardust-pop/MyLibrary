from django.forms import ModelForm
from django import forms

from django.contrib.auth.models import User
# from .models import Order
from django.contrib.auth.forms import UserCreationForm


# class OrderForm(ModelForm):
#     class Meta:
#         model = Order
#         fields = '__all__'

class CreateUserFrom(UserCreationForm):#继承UserCreationFrom
    class Meta:
        #自定义字段
        model = User
        fields = ['username','email','password1','password2']

