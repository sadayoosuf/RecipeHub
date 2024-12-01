from rest_framework import serializers
from .models import Recipe, Review
from django.contrib.auth.models import User


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields =['recipe', 'user', 'rating', 'comment']

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            'id',
            'title',
            'cuisine',
            'meal_type',
            'ingredients',
            'instructions',
            'created_by',
            'reviews'
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','password','email','first_name','last_name']

    def create(self,validated_data):
        u=User.objects.create_user(username=validated_data['username'],password=validated_data['password'],email=validated_data['email'],first_name=validated_data['first_name'],last_name=validated_data['last_name'])

        return u