from django.shortcuts import render
from django.db import models
from django.db import transaction
from django.contrib.auth import authenticate, login
from .models import *
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin
from .serializers import *



class RegisterView(generics.GenericAPIView):

    serializer_class = UserSerializer
    model = User

    def post(self, request):
        """
        Inout: {
                "email":"testadmin100@yopmail.com",
                "first_name":"Test",
                "last_name":"Admin",
                "password":"admin@123"
                }
        Response: {
    "message": "User registered successfully.",
    "data": {
            "id": 12,
            "last_login": null,
            "is_superuser": false,
            "email": "testadmin100@yopmail.com",
            "first_name": "Test",
            "middle_name": null,
            "last_name": "Admin",
            "full_name": "Test Admin",
            "mobile": null,
            "is_staff": false,
            "is_active": false,
            "created_datetime": "2022-11-13T15:36:03.077711Z",
            "updated_datetime": "2022-11-13T15:36:03.143307Z"
            }
        }
        """
        params = request.data
        print(params)

        with transaction.atomic():
            serializer = self.serializer_class(data=params)
            serializer.is_valid(raise_exception=True)
            user_serializer = serializer.save()
            user_serializer.set_password(params['password'])
            user_serializer.save()
        return Response({"message": "User registered successfully.",
                        "data":serializer.data},
                        status=status.HTTP_200_OK)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    def post(self, request):
        """
        Input : {
                    "email":"testadmin100@yopmail.com",
                    "password":"admin@123"
                }
        Response: {
                    "message": "Logged in successfully.",
                    "data": {
                        "id": 13,
                        "email": "suser@yopmail.com",
                        "full_name": " ",
                        "is_active": true,
                        "follow": [
                            2,
                            9
                        ],
                        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxMywidXNlcm5hbWUiOiJzdXNlckB5b3BtYWlsLmNvbSIsImV4cCI6MTY2ODM2MjAxNCwiZW1haWwiOiJzdXNlckB5b3BtYWlsLmNvbSIsIm9yaWdfaWF0IjoxNjY4MzYwMjE0fQ.o6hU1hU61D3_lpOdGr2AM0j5zv2AEUpTN1uKI2H8wT8"
                    }
                }
        """
        params = request.data
        password = params.get('password')
        email = params.get('email')
        if not email or not password:
            return Response({"message": "Email and Password are required !!!!","data":[]},
                        status=status.HTTP_400_BAD_REQUEST)

        try:
            user_obj = User.objects.get(email=email)
            if not user_obj.is_active:
                return Response({"message": "Only Active user can Login","data":[]},
                        status=status.HTTP_400_BAD_REQUEST)
            login(request, user_obj)
            response_data = self.serializer_class(user_obj).data
            return Response({"message": "Logged in successfully.", "data": response_data},
                        status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"message": "User not found with this given Email !!!","data":[]},
                        status=status.HTTP_400_BAD_REQUEST)




class UserListView(generics.GenericAPIView, ListModelMixin):
    permission_classes = (IsAuthenticated, )
    serializer_class = UserSerializer
    
    def post(self, request, *args, **kwargs):
        """
            List the all user
        
        headers : {
                "Authorization" : jwt eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxMiwidXNlcm5hbWUiOiJ0ZXN0YWRtaW4xMDBAeW9wbWFpbC5jb20iLCJleHAiOjE2NjgzNjA1ODgsImVtYWlsIjoidGVzdGFkbWluMTAwQHlvcG1haWwuY29tIiwib3JpZ19pYXQiOjE2NjgzNTg3ODh9.uSpkEuHMnlygPsyWqSHimd0Q9xkCV_8GAvz8n9IeW2c
                  }
        
        """
        try:
            user_obj = User.objects.all()
            serializer_obj=self.serializer_class(user_obj,many=True)
            return Response({"message": "List of Users", "data": serializer_obj.data},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

class FollowTheUser(generics.GenericAPIView):
    # permission_classes = (IsAuthenticated, )
    serializer_class = UserLoginSerializer
    
    def put(self, request, *args, **kwargs):
        """
            Follow the other users
        """
        try:
            print(67)
            params = request.data
            user_id = request.user.pk
            follow_to = params['follow_to']
            user_obj = User.objects.get(pk=user_id)
            print(user_obj)
            user_obj.follow.add(follow_to)
            return Response({"message": "You have started to follow", "data":[]},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

