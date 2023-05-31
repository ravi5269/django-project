from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from users.serializers import UserSerializer
from rest_framework import status

# Create your views here.

from rest_framework_simplejwt.tokens import RefreshToken

################  -----  token id
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication




class RegisterUser(APIView):
    def post(self,request):
        serializer = UserSerializer(data = request.data)
        
        if not serializer.is_valid():
            # print(serializer.errors)
            return Response({'status' : "failed",'errors':serializer.errors,'message':'somthing went worng '},status=status.HTTP_400_BAD_REQUEST)
    
        serializer.save()

        user = User.objects.get(username= serializer.data['username'])
        # token_obj = Token.objects.get_or_create(user= user)

        ###   maualy toke genreate
        refresh = RefreshToken.for_user(user)


        return Response({'status':200,
        'payload':serializer.data, 
        'refresh': str(refresh),
        'access': str(refresh.access_token), 'message' : 'your data is saved'})



class UsersAPIView(APIView):
    authentication_classes = [JWTAuthentication ]
    permission_classes = [IsAuthenticated]


    def get(self, request):
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(
            {"status": "success", "data": serializer.data}, status=status.HTTP_200_OK
        )

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"status": "failed", "data": serializer.data},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def put(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"status": "error", "data": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def patch(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"status": "error", "data": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, pk):
        user = User.objects.get(pk=pk)
        user.delete()
        return Response(
            {"status": "success", "message": "data deleted"},
            status=status.HTTP_200_OK,
        )
