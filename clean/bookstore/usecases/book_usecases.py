from typing import List, Optional
from domain.entities import Book
from interfaces.repositories import BookRepository

class GetAllBooksUseCase:
    def __init__(self, book_repo: BookRepository):
        self.book_repo = book_repo
    
    def execute(self) -> List[Book]:
        return self.book_repo.get_all()

class GetBookByIdUseCase:
    def __init__(self, book_repo: BookRepository):
        self.book_repo = book_repo
    
    def execute(self, book_id: int) -> Optional[Book]:
        return self.book_repo.get_by_id(book_id)
