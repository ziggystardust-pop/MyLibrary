from django.shortcuts import render

# Create your views here.


from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.forms import inlineformset_factory

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,authenticate

from .models import *
# from .forms import OrderForm
# from .filters import OrderFilter

from django.urls import reverse

from django.contrib import messages



def registerPage(request):
    context = {}

    form = UserCreationForm()
    #响应页面的request POST

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        context['form'] = form
        if form.is_valid():

            # if form.
            # user_name = form.username
            # if UserCreationForm.
            form.save()

            return redirect('/')
        else:

        # 请求不是 POST，表明用户正在访问注册页面，展示一个空的注册表单给用户
            context['message'] =  messages.error(request,'快去检查一下两次密码输入是不是一致，或者用户名格式是否正确')
            form = UserCreationForm()

    return render(request,'accounts/register.html',context)


