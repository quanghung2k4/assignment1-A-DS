from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Customer:
    id: Optional[int]
    name: str
    email: str
    password: str
    created_at: Optional[datetime] = None

@dataclass
class Book:
    id: Optional[int]
    title: str
    author: str
    price: float
    stock: int
    created_at: Optional[datetime] = None

@dataclass
class Cart:
    id: Optional[int]
    customer_id: int
    created_at: Optional[datetime] = None

@dataclass
class CartItem:
    id: Optional[int]
    cart_id: int
    book_id: int
    quantity: int
    created_at: Optional[datetime] = None