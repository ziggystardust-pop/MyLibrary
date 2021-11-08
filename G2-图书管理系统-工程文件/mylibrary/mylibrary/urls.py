"""mylibrary URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from library.views import index,BookListView,BookDetailView,AuthorListView
from  accounts.views import *
from library.views import SearchView,BorrowView,ReturnView
urlpatterns = [
    # path('/', include('accounts.urls'), name='index'),
    # path('',registerPage, name='register'),
    path('',index,name = 'index'),
    path('books/',BookListView.as_view(), name='books'),
    path('book/<int:pk>',BookDetailView.as_view(), name='book-detail'),
    path('authors/',AuthorListView.as_view(), name='authors'),

    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('search/', SearchView.as_view(), name='search'),
    path('borrow/', BorrowView.as_view(), name='borrow'),
    path('library/', include('library.urls')),

    path('return/', ReturnView.as_view(), name='return'),

    # path('login/', views.loginPage,name = 'login'),

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
