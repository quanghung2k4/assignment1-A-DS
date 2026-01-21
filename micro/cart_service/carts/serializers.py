from rest_framework import serializers
from .models import Cart, CartItem

class CartItemSerializer(serializers.ModelSerializer):
    book_details = serializers.SerializerMethodField()
    
    class Meta:
        model = CartItem
        fields = ['id', 'book_id', 'quantity', 'book_details']
    
    def get_book_details(self, obj):
        # This will be populated by calling book service
        return None

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Cart
        fields = ['id', 'customer_id', 'created_at', 'items']