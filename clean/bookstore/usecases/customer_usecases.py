from domain.entities import Customer
from interfaces.repositories import CustomerRepository
from django.contrib.auth.hashers import make_password, check_password

class RegisterCustomerUseCase:
    def __init__(self, customer_repo: CustomerRepository):
        self.customer_repo = customer_repo
    
    def execute(self, name: str, email: str, password: str) -> Customer:
        # Hash password
        hashed_password = make_password(password)
        
        # Create customer entity
        customer = Customer(
            id=None,
            name=name,
            email=email,
            password=hashed_password
        )
        
        # Save through repository
        return self.customer_repo.create(customer)

class LoginCustomerUseCase:
    def __init__(self, customer_repo: CustomerRepository):
        self.customer_repo = customer_repo
    
    def execute(self, email: str, password: str) -> Optional[Customer]:
        customer = self.customer_repo.get_by_email(email)
        
        if customer and check_password(password, customer.password):
            return customer
        
        return None
