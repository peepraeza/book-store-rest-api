from django.urls import path
from .views import MemberRegisterView, UserLoginView, MemberInfoView, AdminRegisterView, AdminInfoView

urlpatterns = [
    # member
    path('member/register', MemberRegisterView.as_view()),
    path('member/login', UserLoginView.as_view()),
    path('member/info', MemberInfoView.as_view()),

    path('admin/register', AdminRegisterView.as_view()),
    path('admin/login', UserLoginView.as_view()),
    path('admin/info', AdminInfoView.as_view()),

]
