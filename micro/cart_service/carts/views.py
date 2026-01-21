from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Cart, CartItem
from .serializers import CartSerializer
import requests

# Configuration for other services
CUSTOMER_SERVICE_URL = 'http://localhost:8001/api/customers'
BOOK_SERVICE_URL = 'http://localhost:8002/api/books'

@api_view(['POST'])
def add_to_cart(request):
    customer_id = request.data.get('customer_id')
    book_id = request.data.get('book_id')
    quantity = request.data.get('quantity', 1)
    
    # Verify customer exists by calling customer service
    try:
        customer_response = requests.get(f'{CUSTOMER_SERVICE_URL}/{customer_id}/')
        if customer_response.status_code != 200:
            return Response({'error': 'Customer not found'}, 
                          status=status.HTTP_404_NOT_FOUND)
    except requests.exceptions.RequestException:
        return Response({'error': 'Customer service unavailable'}, 
                       status=status.HTTP_503_SERVICE_UNAVAILABLE)
    
    # Verify book exists by calling book service
    try:
        book_response = requests.get(f'{BOOK_SERVICE_URL}/{book_id}/')
        if book_response.status_code != 200:
            return Response({'error': 'Book not found'}, 
                          status=status.HTTP_404_NOT_FOUND)
    except requests.exceptions.RequestException:
        return Response({'error': 'Book service unavailable'}, 
                       status=status.HTTP_503_SERVICE_UNAVAILABLE)
    
    # Get or create cart
    cart, created = Cart.objects.get_or_create(customer_id=customer_id)
    
    # Add or update cart item
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        book_id=book_id,
        defaults={'quantity': quantity}
    )
    
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
    
    return Response({
        'message': 'Book added to cart',
        'cart_id': cart.id
    }, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def view_cart(request, customer_id):
    try:
        cart = Cart.objects.get(customer_id=customer_id)
    except Cart.DoesNotExist:
        return Response({'items': []})
    
    # Get cart items
    cart_items = CartItem.objects.filter(cart=cart)
    
    # Enrich with book details from book service
    items_data = []
    for item in cart_items:
        try:
            book_response = requests.get(f'{BOOK_SERVICE_URL}/{item.book_id}/')
            if book_response.status_code == 200:
                book_data = book_response.json()
                items_data.append({
                    'id': item.id,
                    'book_id': item.book_id,
                    'quantity': item.quantity,
                    'book': book_data
                })
        except requests.exceptions.RequestException:
            items_data.append({
                'id': item.id,
                'book_id': item.book_id,
                'quantity': item.quantity,
                'book': None
            })
    
    return Response({
        'cart_id': cart.id,
        'customer_id': cart.customer_id,
        'items': items_data
    })
