from django.urls import path
from transaction.views import BookOrderView, TransactionHistoryView

urlpatterns = [
    # transaction
    path('book/order', BookOrderView.as_view()),
    path('admin/transaction', TransactionHistoryView.as_view()),

]
