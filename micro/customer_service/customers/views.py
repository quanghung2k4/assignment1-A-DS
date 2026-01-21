from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Customer
from .serializers import CustomerSerializer
from django.contrib.auth.hashers import check_password

@api_view(['POST'])
def register(request):
    serializer = CustomerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    try:
        customer = Customer.objects.get(email=email)
        if check_password(password, customer.password):
            return Response({
                'message': 'Login successful',
                'customer_id': customer.id,
                'name': customer.name
            })
        return Response({'error': 'Invalid credentials'}, 
                       status=status.HTTP_401_UNAUTHORIZED)
    except Customer.DoesNotExist:
        return Response({'error': 'Customer not found'}, 
                       status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_customer(request, pk):
    try:
        customer = Customer.objects.get(pk=pk)
        return Response({
            'id': customer.id,
            'name': customer.name,
            'email': customer.email
        })
    except Customer.DoesNotExist:
        return Response({'error': 'Customer not found'}, 
                       status=status.HTTP_404_NOT_FOUND)