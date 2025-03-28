from django.urls import path
from .views import RegisterUserView, LoginUserView, VerifyAccountView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('verify-account/', VerifyAccountView.as_view(), name='verify-account'),
    path('login/', LoginUserView.as_view(), name='login'),
]
