from typing import List, Optional
from domain.entities import Customer, Book, Cart, CartItem
from interfaces.repositories import CustomerRepository, BookRepository, CartRepository
from infrastructure.models import CustomerModel, BookModel, CartModel, CartItemModel

class DjangoCustomerRepository(CustomerRepository):
    def create(self, customer: Customer) -> Customer:
        model = CustomerModel.objects.create(
            name=customer.name,
            email=customer.email,
            password=customer.password
        )
        return self._to_entity(model)
    
    def get_by_email(self, email: str) -> Optional[Customer]:
        try:
            model = CustomerModel.objects.get(email=email)
            return self._to_entity(model)
        except CustomerModel.DoesNotExist:
            return None
    
    def get_by_id(self, customer_id: int) -> Optional[Customer]:
        try:
            model = CustomerModel.objects.get(id=customer_id)
            return self._to_entity(model)
        except CustomerModel.DoesNotExist:
            return None
    
    def _to_entity(self, model: CustomerModel) -> Customer:
        return Customer(
            id=model.id,
            name=model.name,
            email=model.email,
            password=model.password,
            created_at=model.created_at
        )

class DjangoBookRepository(BookRepository):
    def get_all(self) -> List[Book]:
        models = BookModel.objects.all()
        return [self._to_entity(m) for m in models]
    
    def get_by_id(self, book_id: int) -> Optional[Book]:
        try:
            model = BookModel.objects.get(id=book_id)
            return self._to_entity(model)
        except BookModel.DoesNotExist:
            return None
    
    def _to_entity(self, model: BookModel) -> Book:
        return Book(
            id=model.id,
            title=model.title,
            author=model.author,
            price=float(model.price),
            stock=model.stock,
            created_at=model.created_at
        )

class DjangoCartRepository(CartRepository):
    def create(self, cart: Cart) -> Cart:
        customer = CustomerModel.objects.get(id=cart.customer_id)
        model = CartModel.objects.create(customer=customer)
        return Cart(id=model.id, customer_id=cart.customer_id, created_at=model.created_at)
    
    def get_by_customer(self, customer_id: int) -> Optional[Cart]:
        try:
            model = CartModel.objects.get(customer_id=customer_id)
            return Cart(id=model.id, customer_id=customer_id, created_at=model.created_at)
        except CartModel.DoesNotExist:
            return None
    
    def add_item(self, cart_item: CartItem) -> CartItem:
        model = CartItemModel.objects.create(
            cart_id=cart_item.cart_id,
            book_id=cart_item.book_id,
            quantity=cart_item.quantity
        )
        return CartItem(
            id=model.id,
            cart_id=cart_item.cart_id,
            book_id=cart_item.book_id,
            quantity=model.quantity,
            created_at=model.created_at
        )
    
    def get_items(self, cart_id: int) -> List[CartItem]:
        models = CartItemModel.objects.filter(cart_id=cart_id)
        return [CartItem(
            id=m.id,
            cart_id=m.cart_id,
            book_id=m.book_id,
            quantity=m.quantity,
            created_at=m.created_at
        ) for m in models]
    
    def get_or_create_item(self, cart_id: int, book_id: int, quantity: int) -> CartItem:
        model, created = CartItemModel.objects.get_or_create(
            cart_id=cart_id,
            book_id=book_id,
            defaults={'quantity': quantity}
        )
        
        if not created:
            model.quantity += quantity
            model.save()
        
        return CartItem(
            id=model.id,
            cart_id=cart_id,
            book_id=book_id,
            quantity=model.quantity,
            created_at=model.created_at
        )
