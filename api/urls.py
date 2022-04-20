from django.urls import path, re_path
from api import views
from .views import RegisterView, LoginView, UserView

urlpatterns = [
    re_path(r'^book$', views.bookApi),
    re_path(r'^book/([0-9]+)$', views.bookApi),
    path('member/register', RegisterView.as_view()),
    path('member/login', LoginView.as_view()),
    path('member/user', UserView.as_view()),
]
