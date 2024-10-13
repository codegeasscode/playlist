from rest_framework import generics, status
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from .serializers import UserSerializer, UserLoginSerializer
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model

User = get_user_model()  

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def create(self, request, *args, **kwargs):
        user_data_list = request.data
        users = []

        for user_data in user_data_list:
            serializer = self.get_serializer(data=user_data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            users.append(user)

        return Response(self.get_serializer(users, many=True).data, status=status.HTTP_201_CREATED)

class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer  
    permission_classes = [AllowAny]  

class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)

            return Response({
                'id': user.id,
                'username': user.username,
                'email': user.email,
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
