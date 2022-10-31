from django.db import models


class Categories(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)


class Genry(models.Model):
    name = models.TextField()
    slug = models.SlugField(unique=True)


class Title(models.Model):
    name = models.CharField(max_length=300)
    year = models.IntegerField()
    description = models.TextField()
    genre = models.ForeignKey(
        Genry,
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True
    )
    category = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True
    )
