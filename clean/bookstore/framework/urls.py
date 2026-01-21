
from django.urls import path
from framework import views

urlpatterns = [
    path('api/accounts/register/', views.register),
    path('api/accounts/login/', views.login),
    path('api/books/', views.book_list),
    path('api/books/<int:pk>/', views.book_detail),
    path('api/cart/add/', views.add_to_cart),
    path('api/cart/<int:customer_id>/', views.view_cart),
]
