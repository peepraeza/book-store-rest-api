from django.urls import path
from .views import CartActionView

urlpatterns = [
    # book
    path('cart/book', CartActionView.as_view()),
    path('cart/book/<book_id>', CartActionView.as_view()),

]
