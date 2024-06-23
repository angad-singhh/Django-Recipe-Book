# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.add_recipe, name="add_recipe"),
    path("add-recipe/", views.add_recipe, name="add_recipe"),
    path("login/", views.login_page, name="login"),
    path("logout/", views.logout_page, name="logout"),
    path("register/", views.register, name="register"),
    path("delete-recipe/<id>/", views.delete_recipe, name="delete"),
    path("view-recipe/", views.view_recipe, name="view_recipe"),
    path("update-recipe/<id>/", views.update_recipe, name="update_recipe"),
]
