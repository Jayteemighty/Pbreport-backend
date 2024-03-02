from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.models import Token


class SignupView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()

    def perform_create(self, serializer):
        password = serializer.validated_data.get('password')
        
        # Hash the password using Django's make_password function
        hashed_password = make_password(password)
        
        # Set the hashed password back to the serializer data
        serializer.validated_data['password'] = hashed_password
        
        user = serializer.save()

        token, created = Token.objects.get_or_create(user=user)

        return Response({'user': serializer.data, 'token': token.key}, status=status.HTTP_201_CREATED)