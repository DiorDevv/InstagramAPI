from django.urls import path
from .views import CreateUserView, VerifyAPIView, GetNewVerification, ChangeInformationsView, ChangeUserPhoto, \
    LoginAPIView, LoginRefreshView, LogOutAPIView

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('login/refresh/', LoginRefreshView.as_view(), name='login_refresh'),
    path('logout/', LogOutAPIView.as_view(), name='logout'),
    path('signup/', CreateUserView.as_view(), name='signup'),
    path('verify/', VerifyAPIView.as_view(), name='verify'),
    path('new-verify/', GetNewVerification.as_view(), name='new-verify'),
    path('change-informations/', ChangeInformationsView.as_view(), name='change-informations'),
    path('change-users/', ChangeUserPhoto.as_view(), name='change-user-photo'),
]
