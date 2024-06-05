from django.urls import path
from .views import *


urlpatterns = [
    # path('HOMFOO-admin-login/',views.adminLogin, name="adminLogin"),
    # path('HOMFOO-admin-logout/',views.adminLogout, name="adminLogout"),


    # path('',views.adminHome, name="adminHome"),
    path('HOMFOO-banner',AdminBanner.as_view(), name="banner"),
    path('HOMFOO-banners',AdminBanners.as_view(), name="banners"),
    path('HOMFOO-delete-banner/<int:id>/',AdminUpdateBanner.as_view(), name="deleteBanner"),
    path('HOMFOO-update-banner/<int:id>/',AdminBannerDelete.as_view(), name="updateBanner"),


    path('HOMFOO-category',AdminCategory.as_view(), name="category"),
    path('HOMFOO-categories',AdminCategories.as_view(), name="categories"),
    path('HOMFOO-update-category/<int:pk>/',AdminUpdateCategory.as_view(), name="updateCategory"),
    path('HOMFOO-delete-category/<int:pk>/',AdminDeleteCategory.as_view(), name="deleteCategory"),


    path('HOMFOO-restaurants',NewRestaurant.as_view(), name="restaurants"),
    path('HOMFOO-restaurant-approval/<int:pk>/',RestaurantApproval.as_view(), name="RestaurantApproval"),
    path('HOMFOO-approved-restaurants',ApprovedRestaurant.as_view(), name="approvedRestaurant"),
    path('HOMFOO-restaurant-rejection/',RestaurantRejection.as_view(), name="RestaurantRejection"),
    path('HOMFOO-rejected-restaurants',RejectedRestaurant.as_view(), name="rejectedRestaurant"),
    path('HOMFOO-remove-restaurant/<int:pk>/',RemoveRestaurant.as_view(), name="RemoveRestaurant"),








]