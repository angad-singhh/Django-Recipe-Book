from django.db import models
from django.contrib.auth.models import User


class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=50)
    description = models.TextField()
    image = models.FileField(upload_to="recipe_images")
