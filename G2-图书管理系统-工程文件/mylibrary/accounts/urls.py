from django.urls import path
from . import views

from django.urls import include

urlpatterns = [
    path('register/',views.registerPage,name = 'register'),

    # path('login/', views.loginPage,name = 'login'),
    path('', include('django.contrib.auth.urls'),name = 'login'),

]
