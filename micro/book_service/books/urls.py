from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list),
    path('<int:pk>/', views.book_detail),
    path('<int:pk>/update-stock/', views.update_stock),
]

# book-service/book_service/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/books/', include('books.urls')),
]