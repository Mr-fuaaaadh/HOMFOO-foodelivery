from django.urls import path
from .views import *


urlpatterns = [
    path('',RestaurantRegistration.as_view(),name="restaurant-register"),
    path('login/',RestaurantLogin.as_view(),name="restourant-login"),


    path('HOMFOO-add-products/',RestaurantAddProduct.as_view(),name="RestaurantAddProduct"),
    path('HOMFOO-shop-products/',RestaurantViewProduct.as_view(),name="RestaurantViewProduct"),
    path('HOMFOO-shop-product-update/<int:pk>/',RestaurantUpdateProduct.as_view(),name="RestaurantUpdateProduct"),
    path('HOMFOO-shop-product-delete/<int:pk>/',RestaurantDeleteProduct.as_view(),name="RestaurantDeleteProduct"),






    

]