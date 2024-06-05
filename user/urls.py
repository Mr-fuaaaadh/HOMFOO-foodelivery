from django.urls import path
from user.views import *


urlpatterns = [
    path('register/',CustomerRegistration.as_view()),
    path('',CustomerLogin.as_view()),


    path('banners/',Banners.as_view()),
    path('categories/',Categories.as_view()),
    path('restaurants/',RestaurantViews.as_view()),
    path('restaurant-product/<int:pk>/',RestaurantBasedProductView.as_view()),
    path('products/',ProductViews.as_view()),




    
]