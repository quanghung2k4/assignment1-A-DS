from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from book.models import Book
from cart.models import Cart
from cartitem.models import CartItem


def _require_customer(request):
    customer_id = request.session.get("customer_id")
    if not customer_id:
        return None
    return customer_id


def add_to_cart(request, book_id):
    customer_id = _require_customer(request)
    if not customer_id:
        messages.info(request, "Please login to add items to cart.")
        return redirect("customer:login")

    book = get_object_or_404(Book, id=book_id)
    qty = int(request.POST.get("quantity", 1)) if request.method == "POST" else 1

    cart = Cart.for_customer(customer_id)

    item, created = CartItem.objects.get_or_create(cart_id=cart.id, book_id=book.id, defaults={"quantity": qty})
    if not created:
        item.quantity += qty
        item.save()

    messages.success(request, f"Added {book.title} to cart.")
    return redirect("book:book_list")


def view_cart(request):
    customer_id = _require_customer(request)
    if not customer_id:
        messages.info(request, "Please login to view cart.")
        return redirect("customer:login")

    cart = Cart.for_customer(customer_id)
    items = CartItem.objects.filter(cart_id=cart.id)
    detailed = []
    total = 0
    for it in items:
        try:
            book = Book.objects.get(id=it.book_id)
        except Book.DoesNotExist:
            continue
        line_total = book.price * it.quantity
        total += line_total
        detailed.append({"item": it, "book": book, "line_total": line_total})

    return render(request, "cart/cart.html", {"items": detailed, "total": total})
from django.shortcuts import render

# Create your views here.
