from rest_framework import serializers
from restaurant.models import *
from .models import *

class CustomerRegisterSerializer(serializers.ModelSerializer):
    class Meta :
        model = Customer
        fields = "__all__"


class CustomerLoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    # You can add additional validation if needed
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if not email:
            raise serializers.ValidationError("email is required")

        if not password:
            raise serializers.ValidationError("Password is required")

        return data


class BannerSeralizer(serializers.ModelSerializer):
    class Meta :
        model = Banner
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta :
        model = Category
        fields = "__all__"


class RestaurantViewSerializer(serializers.ModelSerializer):
    class Meta :
        model = Restaurant
        fields = "__all__"