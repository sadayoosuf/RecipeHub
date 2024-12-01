
from food.models import Recipe,Review
from rest_framework import generics
from food.serializers import RecipeSerializer,ReviewSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.contrib.auth.models import User
from food.serializers import UserSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

class RecipeListCreate(generics.ListCreateAPIView):
    queryset=Recipe.objects.all()
    serializer_class=RecipeSerializer
    # permission_classes = [IsAuthenticated]

class RecipeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    # permission_classes = [IsAuthenticated]


class RecipeSearchAPI(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        query = self.request.query_params.get('search')
        if query:
            recipes = Recipe.objects.filter(
                Q(title__icontains=query) | Q(ingredients__icontains=query) | Q(cuisine__icontains=query))
            recipe_data = RecipeSerializer(recipes, many=True)
            return Response(recipe_data.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "No search query provided"}, status=status.HTTP_400_BAD_REQUEST)

class RecipemealtypeSearchAPI(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        query = self.request.query_params.get('mealtype')
        if query:
            recipes = Recipe.objects.filter(meal_type__icontains=query)
            recipe_data = RecipeSerializer(recipes, many=True)
            return Response(recipe_data.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "No search query provided"}, status=status.HTTP_400_BAD_REQUEST)


class RecipecuisineSearchAPI(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        query = self.request.query_params.get('cuisine')
        if query:
            recipes = Recipe.objects.filter(cuisine__icontains=query)
            recipe_data = RecipeSerializer(recipes, many=True)
            return Response(recipe_data.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "No search query provided"}, status=status.HTTP_400_BAD_REQUEST)

class RecipeingredientsSearchAPI(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        query = self.request.query_params.get('ingredients')
        if query:
            recipes = Recipe.objects.filter(ingredients__icontains=query)
            recipe_data = RecipeSerializer(recipes, many=True)
            return Response(recipe_data.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "No search query provided"}, status=status.HTTP_400_BAD_REQUEST)

class UserAPI(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=UserSerializer


class LogoutView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        self.request.user.auth.token.delete()
        return Response({"msg":"Logout successfully"},status=status.HTTP_200_OK)

# class CreateReview(APIView):
#     permission_classes=[IsAuthenticated]
#     def post(self,request):
#         recipe_name=request.data['title']
#         r=Recipe.objects.get(title=recipe_name)
#
#         u=request.data
#
#         c=request.data['comment']
#         rating=request.data['rating']
#
#         r=Review.objects.create(recipe=r,user=u,rating=rating,comment=c)
#
#         review=ReviewSerializer(r)
#         return Response(review.data,status=status.HTTP_201_CREATED)


class CreateReview(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Get recipe by title
        recipe_name = request.data.get('title')
        try:
            recipe = Recipe.objects.get(title=recipe_name)
        except Recipe.DoesNotExist:
             return Response({"error": "Recipe not found."}, status=status.HTTP_404_NOT_FOUND)

        # Extract data from request
        comment = request.data.get('comment')
        rating = request.data.get('rating')

        # Validate data before creating a review
        if not rating or not comment:
            return Response({"error": "Rating and comment are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Create the Review object
        review = Review.objects.create(recipe=recipe,user=request.user,rating=rating,comment=comment)

        # Serialize the created review and return response
        review_serializer = ReviewSerializer(review)
        return Response(review_serializer.data, status=status.HTTP_201_CREATED)


class ReviewList(APIView):
    def get_object(self,request,pk):
        return Recipe.objects.get(pk=pk)
    def get(self,request,pk):
        r=self.get_object(request,pk)
        review=Review.objects.filter(title=r)
        rev=ReviewSerializer(review.data,many=True)
        return Response(rev.data,status=status.HTTP_200_OK)