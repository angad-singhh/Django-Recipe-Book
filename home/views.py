from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def login_page(request):
    if request.method == "POST":
        data = request.POST
        username = data.get("username")
        password = data.get("password")

        if not User.objects.filter(username=username).exists():
            messages.info(request, "Username is invalid")
            return redirect("/login/")

        user = authenticate(username=username, password=password)

        if user is None:
            messages.info(request, "Password is invalid")
            return redirect("/login/")
        else:
            login(request, user)
            return redirect("/view-recipe/")

    return render(request, "login.html")


def logout_page(request):
    logout(request)
    return redirect("/login/")


def register(request):
    if request.method == "POST":
        data = request.POST
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        username = data.get("username")
        password = data.get("password")

        user = User.objects.filter(username=username)

        if user.exists():
            messages.info(request, "Sorry !! Username is already taken")
            return redirect("/register/")

        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
        )
        # to hash password we use this, rather than directly storing it as string
        user.set_password(password)
        user.save()
        messages.success(request, "Your account is registered")

    return render(request, "register.html")


@login_required(login_url="/login/")
def add_recipe(request):
    if request.method == "POST":
        data = request.POST
        recipe_img = request.FILES.get("image")
        recipe_title = data.get("title")
        recipe_description = data.get("description")

        Recipe.objects.create(
            title=recipe_title, description=recipe_description, image=recipe_img
        )

        return redirect("/")

    return render(request, "add_recipe.html")


@login_required(login_url="/login/")
def delete_recipe(request, id):
    queryset = Recipe.objects.get(id=id)
    queryset.delete()

    return redirect("/view-recipe/")


def view_recipe(request):
    queryset = Recipe.objects.all()

    if request.GET.get("search_term"):
        queryset = queryset.filter(title__icontains=request.GET.get("search_term"))

    context = {"Recipes": queryset}

    return render(request, "view_recipe.html", context)


@login_required(login_url="/login/")
def update_recipe(request, id):
    queryset = Recipe.objects.get(id=id)
    context = {"recipe": queryset}

    if request.method == "POST":
        data = request.POST
        recipe_img = request.FILES.get("image")
        recipe_title = data.get("title")
        recipe_description = data.get("description")

        queryset.title = recipe_title
        queryset.description = recipe_description

        if recipe_img:
            queryset.image = recipe_img

        queryset.save()
        return redirect("/view-recipe/")

    return render(request, "update.html", context)
