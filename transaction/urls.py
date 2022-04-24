from django.urls import path
# from .views import MemberRegisterView, MemberLoginView, MemberInfoView
from transaction.views import BookOrderView, TransactionHistoryView

urlpatterns = [
    # transaction
    path('book/order', BookOrderView.as_view()),
    path('admin/transaction', TransactionHistoryView.as_view()),

]
