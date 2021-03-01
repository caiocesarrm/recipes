from rest_framework import serializers
from abrecipes.recipes.models import *

class IngredientSerializer(serializers.ModelSerializer):
    metric_display = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Ingredient
        fields = '__all__'
        exclude = []

    def get_metric_display(self,obj):
        return obj.get_metric_display()

class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient_metric = serializers.SerializerMethodField(read_only=True)
    ingredient_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = RecipeIngredient
        exclude = ['recipe', 'id']

    def get_ingredient_metric(self, obj):
        return obj.ingredient.metric

    def get_ingredient_name(self, obj):
        return obj.ingredient.name

class RecipeSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer(many=True, source='recipe_ingredient')

    class Meta:
        model = Recipe
        fields = '__all__'
        exclude = []

    #it's not necessary to use a nested serializer for insertion/update
    #to avoid multiple requests i've decided to use nested insertion
    #also, i believe that creating a recipe without ingredientes don't make sense
    def create(self, validated_data):
        recipe_ingredient = validated_data.pop('recipe_ingredient')
        recipe = Recipe.objects.create(**validated_data)
        for ingredient in recipe_ingredient:
            RecipeIngredient.objects.create(recipe=recipe, **ingredient)
            
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('recipe_ingredient')
        new_ingredients_ids = [i['ingredient'].id for i in ingredients]

        recipe_ingredients = RecipeIngredient.objects.filter(recipe=instance).select_related('ingredient')
        old_ingredients_ids = [i.ingredient.id for i in recipe_ingredients]

        for ri in recipe_ingredients:
            if ri.ingredient.id not in new_ingredients_ids:
                ri.delete()

        for i in ingredients:
            if i['ingredient'].id not in old_ingredients_ids:
                RecipeIngredient.objects.create(recipe=instance, **i)
            else:
                RecipeIngredient.objects.filter(recipe=instance, ingredient=i['ingredient'].id).update(amount=i['amount'])

        return instance