from django.db import models

UNIT_CHOICES = (
    ("ct", "centiliters"),
    ("lt", "liters"),
    ("g", "grams"),
    ("kg", "kilograms"),
    ("un", "units"),
    )

class Ingredient(models.Model):
    name = models.CharField(max_length=2000)
    article_number = models.CharField(max_length=20, unique=True)
    cost = models.DecimalField(max_digits=12, decimal_places=2)
    metric = models.CharField(choices=UNIT_CHOICES, max_length=6)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    amount_per_cost = models.FloatField()

    class Meta:
        db_table = 'ingredient'
        default_permissions = ('add', 'change', 'delete', 'view')

    def save(self, *args, **kwargs):
        super(Ingredient, self).save(*args, **kwargs) 


class Recipe(models.Model):
    name = models.CharField(max_length=2000)
    price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')
    instructions = models.TextField()
    #set default image to avoid the burden of search for an image everytime a new recipe is created
    #only for demonstration purposes, not a production scenario
    image_url = models.CharField(max_length=500, default="https://twisper.com/wp-content/uploads/2020/03/close-up-photo-of-burger-3915906-scaled.jpg")
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        db_table = 'recipe'
        default_permissions = ('add', 'change', 'delete', 'view')

    def get_ingredients_cost(self):
        costs = []
        for ingredient in RecipeIngredient.objects.filter(recipe=self.id).select_related('ingredient'):
            costs.append(ingredient.get_ingredient_cost())
        return sum(costs)


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipe_ingredient')
    amount = models.FloatField()

    class Meta:
        db_table = 'recipe_ingredient'
        default_permissions = ('add', 'change', 'delete', 'view')

    def get_ingredient_cost(self):
        return float(self.ingredient.cost)*self.amount/self.ingredient.amount_per_cost