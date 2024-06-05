from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
from .serializers import *
from restaurant.serializers import *
from datetime import datetime, timedelta
import jwt
from restaurant.models import *
from .models import *

from django.conf import settings
# Create your views here.




class CustomerRegistration(APIView):
    
    def post(self,request):
        serializer = CustomerRegisterSerializer(data=request.data)
        if serializer.is_valid():
            hashed_password = make_password(serializer.validated_data['password'])
            serializer.validated_data['password'] = hashed_password
            serializer.save()
            return Response({"status":"Registration success","data": serializer.data},status=200)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class CustomerLogin(APIView):
    def post(self, request):
        serializer = CustomerLoginSerializer(data=request.data)
        
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            user = Customer.objects.filter(email=email).first()
            
            if user and check_password(password, user.password):
                payload = {
                    'user_id': user.pk,
                    'exp': datetime.utcnow() + timedelta(minutes=60),
                    'iat': datetime.utcnow()
                }
                
                # Encode JWT token
                token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
                print(token)

                response_data = {
                    "status":"User Login is Successfully Completed",
                    "token": token,
                    "User_ID" : user.pk,
                    "data" : serializer.data
                }
                return Response(response_data,status=200)
                
                response.set_cookie('token', token, expires=datetime.utcnow() + timedelta(minutes=60), secure=True)
                
                return response
            else:
                return Response({"status": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Banners(APIView):
    def get(self,request):
        try :
            banners = Banner.objects.all()
            serializer = BannerSeralizer(banners,many=True)
            return Response({"status": "Banners fetching is successful", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "An error occurred", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class Categories(APIView):
    def get(self,request):
        try :
            category = Category.objects.all()
            serializer = CategorySerializer(category,many=True)
            return Response({"status": "Category fetching is successful", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "An error occurred", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RestaurantViews(APIView):
    def get(self, request):
        try:
            restaurants = Restaurant.objects.filter(status="Approved")
            serializer = RestaurantViewSerializer(restaurants, many=True)
            return Response({"status": "Restaurant fetching is successful", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "An error occurred", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RestaurantBasedProductView(APIView):
    def post(self, request, pk):
        try:
            token = request.headers.get("Authorization")
            print(token)
            if token is None:
                return Response({"status": "Invalid Token"}, status=status.HTTP_401_UNAUTHORIZED)
                
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = Customer.objects.filter(pk=payload['user_id']).first()
            if user is None:
                print("kllam")
                return Response({"status": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)

            restaurant = Restaurant.objects.filter(pk=pk).first()
            print(restaurant)
            if not restaurant:
                return Response({"status": "Error", "message": "Restaurant not found"}, status=status.HTTP_404_NOT_FOUND)

            products = Product.objects.filter(restaurant=restaurant)
            serializer = ProductSerializer(products, many=True)
            return Response({"status": "Restaurant Based Product Fetching Successfully completed", "data": serializer.data}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({"status": "error", "message": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({"status": "error", "message": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
        except AuthenticationFailed as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"status": "An error occurred", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ProductViews(APIView):
    def get(self, request):
        try:
            products = Product.objects.all()
            serializer = ProductSerializer(products, many=True)
            return Response({"status": "product fetching is successful", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "An error occurred", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
