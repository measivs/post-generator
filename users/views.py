from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import UserRegistrationSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken



# Create your views here.

User = get_user_model()

class RegisterUserView(GenericAPIView):
    """
    A view for user registration.

    Allows new users to register by providing necessary details
    and stores their information in the database.

    Permissions:
        - Publicly accessible.

    POST:
        - Registers a new user.
    """
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            'user_id': user.id,
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }, status=status.HTTP_201_CREATED)
    

class VerifyAccountView(GenericAPIView):
    """
    A view for account verification.
    Requires a valid JWT token in the Authorization header.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        user.is_verified = True
        user.save()
        
        return Response({
            "message": "Account verified successfully"
        }, status=status.HTTP_200_OK)
    

class LoginUserView(TokenObtainPairView):
    """
        A view for user login.

        Allows authenticated users to log in using their credentials.

        Permissions:
            - Publicly accessible.
    """
    serializer_class = CustomTokenObtainPairSerializer
