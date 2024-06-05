from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.exceptions import NotFound
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from restaurant.serializers import *
from datetime import datetime, timedelta
import jwt
from django.template.loader import render_to_string
from restaurant.models import *
from .models import *
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth.models import User
# Create your views here.


# def adminLogin(request):
#     if request.user.is_authenticated :
#         return redirect('adminHome')
#     else :

       

#         if request.method == 'POST':
#             username = request.POST.get('username')
#             password = request.POST.get('password')

#             user = authenticate(username = username, password = password)

#             if user is not None:
#                 login(request, user)
#                 return redirect('adminHome')
#             else:
#                 messages.error(request, "username or password is incorrect")
#                 return redirect('adminLogin')

#         return render(request, 'login.html')


# def adminLogout(request):
#     logout(request)
#     return redirect('adminLogin')




# def adminHome(request):
#     if request.user.is_authenticated:
#         return render(request, 'index-2.html')
#     else:
#         return redirect('adminLogin')

class AdminBanner(APIView):
    def post(self, request):
        try:
            serializer = AdminBannerSerializers(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class AdminBanners(APIView):
    def get(self, request):
        try:
            banners = Banner.objects.all()
            serializer = AdminBannerSerializers(banners, many=True)
            return Response({"status": "Banners fetching is successful", "Banners": serializer.data})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class AdminBannerDelete(APIView):
    def get(self, request, pk):
        try:
            banner_instance = Banner.objects.filter(pk=pk).first()
            if banner_instance:
                serializer = AdminBannerSerializers(banner_instance)
                return Response(serializer.data)
            else:
                return Response({"status": "Banner not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        try:
            banner_instance = Banner.objects.filter(pk=pk).first()
            if banner_instance:
                banner_instance.delete()
                return Response({"status": "Banner deleted successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "Banner not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AdminUpdateBanner(APIView):
    def get(self, request, pk):
        try:
            banner_instance = Banner.objects.filter(pk=pk).first()
            if banner_instance:
                serializer = AdminBannerSerializers(banner_instance)
                return Response(serializer.data)
            else:
                return Response({"status": "Banner not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self, request, pk):
        try:
            banner_instance = Banner.objects.filter(pk=pk).first()
            if banner_instance:
                serializer = AdminBannerSerializers(banner_instance, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"status": "Banner updated successfully"}, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Banner data is invalid"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"status": "Banner not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




########################################  CATEGORY ##########################################


class AdminCategory(APIView):
    def post(self, request):
        try:
            serializer = AdminCategorySerializers(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "Category created successfully"}, status=status.HTTP_201_CREATED)
            else :
                return Response({"error": "Category data is invalid"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e :
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class AdminCategories(APIView):
    def get(self, request):
        try:
            categories = Category.objects.all()
            serializer = AdminCategorySerializers(categories, many=True)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AdminUpdateCategory(APIView):
    def get(self, request, pk):
        try:
            category = Category.objects.filter(pk=pk).first()
            if category:
                serializer = AdminCategorySerializers(category)
                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
            else:
                raise NotFound("Category not found")
        except NotFound as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk):
        try:
            category = Category.objects.filter(pk=pk).first()
            if category:
                serializer = AdminCategorySerializers(category, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"status": "Category updated successfully"}, status=status.HTTP_200_OK)
                else:
                    return Response({"status": "error", "message": "Category data is invalid"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                raise NotFound("Category not found")
        except NotFound as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class AdminDeleteCategory(APIView):
    def get(self, request, pk):
        try:
            category = Category.objects.filter(pk=pk).first()
            if category:
                serializer = AdminCategorySerializers(category)
                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
            else:
                raise NotFound("Category not found")
        except NotFound as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        try:
            category = Category.objects.filter(pk=pk).first()
            if category:
                category.delete()
                return Response({"status": "Category deleted successfully"}, status=status.HTTP_200_OK)
            else:
                raise NotFound("Category not found")
        except NotFound as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






#########################     Restaurant Approval    ##############################


class NewRestaurant(APIView):
    def get(self, request):
        try:
            restaurants = Restaurant.objects.filter(status="Pending")
            serializer = RestaurantSerializer(restaurants, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"message": "An error occurred while retrieving restaurants: {}".format(str(e))})


class RemoveRestaurant(APIView):
    def get(self,request,pk):
        try :
            restaurant = Restaurant.objects.filter(pk=pk).first()
            if restaurant:
                serializer = RestaurantSerializer(restaurant)
                return Response(serializer.data)
            else :
                return Response({"message": "Restaurant not found"})
        except Exception as e :
            return Response({"message": "An error occurred while retrieving restaurant: {}".format(str(e))})

    def delete(self, request, pk):
        try:
            restaurant = Restaurant.objects.filter(pk=pk).first()
            if restaurant:
                restaurant.delete()
                return Response({"message": "Restaurant deleted successfully"})
            else :
                return Response({"message": "Restaurant not found"})
        except Exception as e :
            return Response({"message": "An error occurred while deleting restaurant: {}".format(str(e))})

def restaurantApproval_mail(email,seller_info):
    subject = "Your restaurant has been approved by the admin"
    html_content = render_to_string('approval.html',{"seller_info":seller_info})
    
    email = EmailMessage(
        subject = subject,
        body = html_content,
        from_email = 'muhammadfuhad3@gmail.com',
        to = [email],

    )

    email.content_subtype = 'html'
    email.send()

class RestaurantApproval(APIView):
    def put(self, request, pk):
        try:
            seller_info = Restaurant.objects.filter(pk=pk).first()
            if seller_info and seller_info.status != "Approved":
                seller_info.status = "Approved"
                seller_info.save()
                restaurantApproval_mail(seller_info.email, seller_info)  # Attempt to send email
                return Response({"message": "Restaurant Approved"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Restaurant is already approved"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": "An error occurred while approving restaurant: {}".format(str(e))}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class RestaurantRejection(APIView):
    def put(self,request,pk):
        try :
            seller_info = Restaurant.objects.filter(pk=pk).first()
            if seller_info and seller_info.status != "Rejected":
                seller_info.status = "Rejected"
                seller_info.save()
                return Response({"message": "Restaurant Rejected"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Restaurant is already rejected"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": "An error occurred while approving restaurant: {}".format(str(e))}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class ApprovedRestaurant(APIView):
    def get(self,request):
        try:
            restaurant = Restaurant.objects.filter(status="Approved")
            serializer = RestaurantSerializer(restaurant, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"message": "An error occurred while retrieving restaurants: {}".format(str(e))})



class RejectedRestaurant(APIView):
    def get(self,request):
        try :
            restaurant = Restaurant.objects.filter(status="Rejected")
            serializer = RestaurantSerializer(restaurant, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"message": "An error occurred while retrieving restaurants: {}".format(str(e))})