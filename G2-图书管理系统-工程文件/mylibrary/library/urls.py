from django.urls import path
from library import views

urlpatterns = [
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),

]
