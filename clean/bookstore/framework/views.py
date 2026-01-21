from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from usecases.customer_usecases import RegisterCustomerUseCase, LoginCustomerUseCase
from usecases.book_usecases import GetAllBooksUseCase, GetBookByIdUseCase
from usecases.cart_usecases import AddToCartUseCase, ViewCartUseCase
from infrastructure.repository_impl import (
    DjangoCustomerRepository, DjangoBookRepository, DjangoCartRepository
)

# Initialize repositories
customer_repo = DjangoCustomerRepository()
book_repo = DjangoBookRepository()
cart_repo = DjangoCartRepository()

@api_view(['POST'])
def register(request):
    use_case = RegisterCustomerUseCase(customer_repo)
    try:
        customer = use_case.execute(
            name=request.data['name'],
            email=request.data['email'],
            password=request.data['password']
        )
        return Response({
            'id': customer.id,
            'name': customer.name,
            'email': customer.email
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    use_case = LoginCustomerUseCase(customer_repo)
    customer = use_case.execute(
        email=request.data['email'],
        password=request.data['password']
    )
    
    if customer:
        return Response({
            'message': 'Login successful',
            'customer_id': customer.id,
            'name': customer.name
        })
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def book_list(request):
    use_case = GetAllBooksUseCase(book_repo)
    books = use_case.execute()
    return Response([{
        'id': b.id,
        'title': b.title,
        'author': b.author,
        'price': b.price,
        'stock': b.stock
    } for b in books])

@api_view(['GET'])
def book_detail(request, pk):
    use_case = GetBookByIdUseCase(book_repo)
    book = use_case.execute(pk)
    
    if book:
        return Response({
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'price': book.price,
            'stock': book.stock
        })
    return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def add_to_cart(request):
    use_case = AddToCartUseCase(cart_repo)
    try:
        result = use_case.execute(
            customer_id=request.data['customer_id'],
            book_id=request.data['book_id'],
            quantity=request.data.get('quantity', 1)
        )
        return Response(result, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def view_cart(request, customer_id):
    use_case = ViewCartUseCase(cart_repo)
    result = use_case.execute(customer_id)
    return Response(result)
