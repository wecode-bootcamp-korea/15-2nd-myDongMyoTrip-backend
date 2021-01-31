import requests

from rest_framework                 import serializers, status
from rest_framework.views           import APIView
from rest_framework.response        import Response

from .models                        import User
from .serializers                   import SignUpSerializer, UserSerializer

class UserSignUpView(APIView):
    def post(self, request, format=None):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserSignInView(APIView):
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            if User.objects.filter(email=serializer.data['email']).exists():
                user = User.objects.get(email=serializer.data['email'])
                if user.password == serializer.data['password']:   
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.data, status=status.HTTP_401_UNAUTHORIZED) 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
