from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'price', 'stock']

# book-service/books/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Book
from .serializers import BookSerializer

@api_view(['GET'])
def book_list(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def book_detail(request, pk):
    try:
        book = Book.objects.get(pk=pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)
    except Book.DoesNotExist:
        return Response({'error': 'Book not found'}, 
                       status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def update_stock(request, pk):
    try:
        book = Book.objects.get(pk=pk)
        quantity = request.data.get('quantity', 0)
        book.stock -= quantity
        book.save()
        return Response({'stock': book.stock})
    except Book.DoesNotExist:
        return Response({'error': 'Book not found'}, 
                       status=status.HTTP_404_NOT_FOUND)