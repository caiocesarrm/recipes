
from django.conf.urls import url, include
from django.urls import path
from . import views

urlpatterns = [
    #api
    path('api/recipes/<int:pk>/', views.RecipeDetailUpdateDelete.as_view()),
    
    path('api/recipes/', views.RecipeListCreate.as_view()),

    path('api/ingredients/<int:pk>/', views.IngredientDetailUpdateDelete.as_view()),
    
    path('api/ingredients/', views.IngredientListCreate.as_view()),

    #templates
    path('recipes/<int:pk>/', views.RecipeDetail.as_view(), name='recipe_detail'),
    
    path('recipes/', views.RecipeList.as_view(), name='recipe_list'),

    path('recipes/<int:pk>/edit/', views.RecipeForm.as_view(), name='recipe_edit'),

    path('recipes/new/', views.RecipeForm.as_view(), name='recipe_create'),

    path('ingredients/', views.IngredientList.as_view(), name='ingredient_list'),

    path('ingredients/<int:pk>/edit/', views.IngredientForm.as_view(), name='ingredient_edit'),

    path('ingredients/new/', views.IngredientForm.as_view(), name='ingredient_create'),
    
]