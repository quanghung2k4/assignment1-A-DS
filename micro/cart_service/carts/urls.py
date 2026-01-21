from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_to_cart),
    path('<int:customer_id>/', views.view_cart),
]

# cart-service/cart_service/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/cart/', include('carts.urls')),