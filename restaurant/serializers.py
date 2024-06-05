from rest_framework import serializers
from .models import *



class RestaurantRegisterSerializer(serializers.ModelSerializer):
    class Meta :
        model = Restaurant
        fields = ['name','owner_name','phone','email','location','password','image','longitude','latitude']




class RestaurantLoginSerializer(serializers.ModelSerializer):
    
    email = serializers.CharField()
    password = serializers.CharField()

    class Meta :
        model = Restaurant
        fields = ['email','password','id']

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if not email:
            raise serializers.ValidationError("email is required")

        if not password:
            raise serializers.ValidationError("Password is required")

        return data




class ProductSerializer(serializers.ModelSerializer):
    class Meta :
        model = Product
        fields = '__all__'