from domain.entities import Cart, CartItem
from interfaces.repositories import CartRepository
from typing import List, Dict

class AddToCartUseCase:
    def __init__(self, cart_repo: CartRepository):
        self.cart_repo = cart_repo
    
    def execute(self, customer_id: int, book_id: int, quantity: int) -> Dict:
        # Get or create cart
        cart = self.cart_repo.get_by_customer(customer_id)
        
        if not cart:
            cart = self.cart_repo.create(Cart(
                id=None,
                customer_id=customer_id
            ))
        
        # Add item to cart
        cart_item = self.cart_repo.get_or_create_item(cart.id, book_id, quantity)
        
        return {
            'cart_id': cart.id,
            'item_id': cart_item.id,
            'message': 'Book added to cart'
        }

class ViewCartUseCase:
    def __init__(self, cart_repo: CartRepository):
        self.cart_repo = cart_repo
    
    def execute(self, customer_id: int) -> Dict:
        cart = self.cart_repo.get_by_customer(customer_id)
        
        if not cart:
            return {'items': []}
        
        items = self.cart_repo.get_items(cart.id)
        
        return {
            'cart_id': cart.id,
            'items': items
        }