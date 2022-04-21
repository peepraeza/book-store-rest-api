from django.urls import path
from .views import BookActionView

urlpatterns = [
    # book
    path('book', BookActionView.as_view()),
    path('admin/book', BookActionView.as_view()),
    path('admin/book/<book_id>', BookActionView.as_view()),

]
