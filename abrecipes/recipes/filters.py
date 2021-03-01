from django_filters import rest_framework as filters

class RecipeSearch(filters.FilterSet):
    name = filters.CharFilter(field_name='name',lookup_expr='icontains')

class IngredientSearch(filters.FilterSet):
    name = filters.CharFilter(field_name='name',lookup_expr='icontains')
    article_number = filters.CharFilter(field_name='article_number',lookup_expr='icontains')