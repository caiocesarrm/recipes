from django.views.generic import ListView, DetailView, TemplateView
from abrecipes.recipes.models import Recipe, Ingredient, UNIT_CHOICES
from abrecipes.recipes.filters import IngredientSearch, RecipeSearch
from rest_framework import generics
from abrecipes.recipes.serializers import RecipeSerializer, IngredientSerializer
from abrecipes.recipes.models import Ingredient, Recipe
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.shortcuts import get_object_or_404
from abrecipes.recipes.tasks import send_email
from django.conf import settings

# api
class IngredientDetailUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    lookup_fields = ['id']

class IngredientListCreate(generics.ListCreateAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name', 'article_number']
    search_fields = ['name', 'article_number']
    filterset_class = IngredientSearch

class RecipeDetailUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    lookup_fields = ['pk']
 
class RecipeListCreate(generics.ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name']
    search_fields = ['name']
    filterset_class = RecipeSearch

    def perform_create(self, serializer):
        recipe = serializer.save()
        #here we could send an email to some manager notifiyng that a new recipe was created
        #send_email.apply_async(args=[recipe.id], priority=10, queue=f'email_{settings.ENV}')

        
# templates
class RecipeList(ListView):
    model = Recipe
    context_object_name = 'recipes'

class RecipeDetail(DetailView):
    model = Recipe
    context_object_name = 'recipe'

class RecipeForm(TemplateView):
    template_name = "recipes/recipe_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs.get('pk'):
            context['recipe'] = get_object_or_404(Recipe, pk=self.kwargs.get('pk'))
        context['ingredients'] = Ingredient.objects.all()
        context['unit_choices'] = UNIT_CHOICES
        return context

class IngredientList(ListView):
    model = Ingredient
    template_name = "ingredients/ingredient_list.html"
    context_object_name = 'ingredients'

class IngredientForm(TemplateView):
    template_name = "ingredients/ingredient_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs.get('pk'):
            context['ingredient'] = get_object_or_404(Ingredient, pk=self.kwargs.get('pk'))
        context['unit_choices'] = UNIT_CHOICES
        return context