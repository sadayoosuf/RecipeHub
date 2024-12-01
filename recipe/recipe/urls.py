"""
URL configuration for recipe project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from food import views
from rest_framework.routers import SimpleRouter
router=SimpleRouter()

router.register('users',views.UserAPI)
from rest_framework.authtoken import views as view1

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.RecipeListCreate.as_view()),
    path('fooddetail/<int:pk>',views.RecipeDetail.as_view()),
    path('search/',views.RecipeSearchAPI.as_view()),
    path('mealtype/',views.RecipemealtypeSearchAPI.as_view()),
    path('cusine/',views.RecipecuisineSearchAPI.as_view()),
    path('ingredients/',views.RecipeingredientsSearchAPI.as_view()),
    path('user/', include(router.urls)),
   path('login/',view1.obtain_auth_token),
    path('logout/',views.LogoutView.as_view()),
    path('createreview/',views.CreateReview.as_view()),
    path('listreview/',views.ReviewList.as_view()),

]
