from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CustomUserSerializer, UserProfileSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from .models import NewUser
import json

class CustomUserCreate(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format='json'):
        serializer = CustomUserSerializer(data=request.data)
        print(request.data["user_name"])
        existingUserEmail = NewUser.objects.filter(email=request.data["email"])
        existingUserUsername = NewUser.objects.filter(user_name = request.data["user_name"])
        print(existingUserUsername)
        if(existingUserEmail or existingUserUsername ):
            return Response({"error":"User with this email or user name already exists"}, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            newuser = serializer.save()
            if newuser:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileDetailAPIView(APIView):

    def get_object(self, pk):
        try:
            return NewUser.objects.get(pk=pk)
        except NewUser.DoesNotExist:
            raise status.HTTP_400_BAD_REQUEST

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        print(snippet)
        serializer = UserProfileSerializer(snippet)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        userserializer = CustomUserSerializer(request.user)
        user = userserializer.data
        user = json.dumps(user)
        loggedInUser = json.loads(user) 
        print("loggedIn user",loggedInUser["id"])
        print(request.data)
        snippet = self.get_object(pk)
        if(loggedInUser["id"] != request.data["id"]):
            return Response({"error" : "different user operation not possible"}, status = status.HTTP_400_BAD_REQUEST)

        serializer = UserProfileSerializer(snippet, data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
