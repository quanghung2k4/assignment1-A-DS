from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities import Customer, Book, Cart, CartItem

class CustomerRepository(ABC):
    @abstractmethod
    def create(self, customer: Customer) -> Customer:
        pass
    
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[Customer]:
        pass
    
    @abstractmethod
    def get_by_id(self, customer_id: int) -> Optional[Customer]:
        pass

class BookRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Book]:
        pass
    
    @abstractmethod
    def get_by_id(self, book_id: int) -> Optional[Book]:
        pass

class CartRepository(ABC):
    @abstractmethod
    def create(self, cart: Cart) -> Cart:
        pass
    
    @abstractmethod
    def get_by_customer(self, customer_id: int) -> Optional[Cart]:
        pass
    
    @abstractmethod
    def add_item(self, cart_item: CartItem) -> CartItem:
        pass
    
    @abstractmethod
    def get_items(self, cart_id: int) -> List[CartItem]:
        pass
    
    @abstractmethod
    def get_or_create_item(self, cart_id: int, book_id: int, quantity: int) -> CartItem:
        pass
