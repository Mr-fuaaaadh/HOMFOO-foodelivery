from rest_framework import serializers
from user.models import *
from restaurant.models import *






class AdminBannerSerializers(serializers.ModelSerializer):
    class Meta :
        model = Banner
        fields = "__all__"



class AdminCategorySerializers(serializers.ModelSerializer):
    class Meta :
        model = Category
        fields = "__all__"


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = "__all__"