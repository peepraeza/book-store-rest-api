from django.urls import path
# from .views import MemberRegisterView, MemberLoginView, MemberInfoView
from transaction.views import BookBuyView

urlpatterns = [
    # transaction
    path('book/buy', BookBuyView.as_view()),
    # path('admin/transaction', TransactionView.as_view()),

]
