from django.urls import include, path
from django.shortcuts import redirect

urlpatterns = [
    path("", lambda request: redirect('recipes/', permanent=False)),
    path("", include(("abrecipes.recipes.urls", "abrecipes.recipes"), namespace="recipes")),
]

