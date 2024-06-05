from django.shortcuts import render
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from datetime import datetime, timedelta
from datetime import datetime, timedelta
import jwt
from django.shortcuts import get_object_or_404
from .models import *
from django.conf import settings
# Create your views here.


class RestaurantRegistration(APIView):
    def post(self,request):
        serializer = RestaurantRegisterSerializer(data=request.data)
        if serializer.is_valid():
            hashed_password = make_password(serializer.validated_data['password'])
            serializer.validated_data['password'] = hashed_password
            serializer.save()
            return Response({"status":"Registration success","data": serializer.data},status=200)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        



class RestaurantLogin(APIView):
    def post(self, request):
        serializer = RestaurantLoginSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            restaurant = Restaurant.objects.filter(email=email, status="Approved").first()
            if restaurant and check_password(password, restaurant.password):
                payload = {
                    'id': restaurant.pk,
                    'exp': datetime.utcnow() + timedelta(minutes=60),
                    'iat': datetime.utcnow()
                }

                token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
                print(token)

                response = Response({
                    "status": "login success",
                    "data": serializer.data,
                    "user_id": restaurant.pk ,
                    "token": token
                }, status=200)
                
                response.set_cookie('token', token, expires=datetime.utcnow() + timedelta(minutes=60), secure=True)
                
                return response
            else:
                return Response({"status": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RestaurantAddProduct(APIView):
    def post(self, request):
        try:
            token = request.headers.get('Authorization')
            print("token   :",token)
            if token is None:
                return Response({"status": "error", "message": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)

            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            restaurant = Restaurant.objects.filter(pk=payload['id']).first()
            print(restaurant)
            
            if not restaurant:
                raise AuthenticationFailed('User not found!')
            
            owner_data = request.data.copy()
            owner_data['restaurant'] = restaurant.pk
                
            serializer = ProductSerializer(data=owner_data)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success", "message": "Product added successfully", "data": serializer.data}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token has expired'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
        except AuthenticationFailed as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RestaurantViewProduct(APIView):
    def post(self, request):
        try:
            token = request.headers.get('Authorization')
            print("token  :",token)
            if token is None:
                return Response({"status": "error", "message": "Unauthenticated"}, status=200)
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            restaurant_user = Restaurant.objects.filter(pk=payload['id']).first()
            if not restaurant_user:
                raise AuthenticationFailed('User not found!')

            products = Product.objects.filter(restaurant=restaurant_user)
            serializer = ProductSerializer(products, many=True)
            return Response({"status": "Product Fetching is successful", "data": serializer.data}, status=200)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token has expired'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
        except AuthenticationFailed as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
class RestaurantUpdateProduct(APIView):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product)
        return Response({"status": "Product Fetching is successful", "data": serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            token = request.headers.get('Authorization')
            print("token  :",token)
            if not token:
                return Response({"status": "error", "message": "Authorization token is missing"}, status=status.HTTP_401_UNAUTHORIZED)

            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            restaurant = Restaurant.objects.filter(pk=payload.get('id')).first()
            if not restaurant:
                raise AuthenticationFailed('User not found!')
            
            # Ensure that the product being updated belongs to the authenticated restaurant
            product = Product.objects.filter(pk=pk, restaurant=restaurant).first()
            print(product)
            if not product:
                return Response({"status": "error", "message": "Product not found or does not belong to the authenticated restaurant"}, status=status.HTTP_404_NOT_FOUND)
            
            # Update the serializer with the request data
            serializer = ProductSerializer(product, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()  # Save the updated data
            print("save")
            return Response({"status": "success", "message": "Product updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token has expired'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
        except AuthenticationFailed as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except ValidationError as e:
            return Response({'error': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class RestaurantDeleteProduct(APIView):
    def delete(self, request, pk):
        try:
            token = request.headers.get('Authorization')
            if not token:
                return Response({"status": "error", "message": "Authorization token is missing"}, status=status.HTTP_401_UNAUTHORIZED)

            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            restaurant = Restaurant.objects.filter(pk=payload.get('id')).first()

            if not restaurant:
                raise AuthenticationFailed('User not found!')

            product = get_object_or_404(Product, pk=pk)
            product.delete()
            serializer = ProductSerializer(product)
            
            return Response({"status": "success", "message": "Product deleted successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({"status": "error", "message": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({"status": "error", "message": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
        except Product.DoesNotExist:
            return Response({"status": "error", "message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        except AuthenticationFailed as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
