from django.urls import path
# from .views import MemberRegisterView, MemberLoginView, MemberInfoView
from appconfig.views import AppConfigView

urlpatterns = [
    # # update app config
    path('admin/update/point-ratio', AppConfigView.as_view()),

]
