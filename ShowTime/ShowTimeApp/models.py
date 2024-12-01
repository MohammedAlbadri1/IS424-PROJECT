from django.db import models

class movies(models.Model):
    title = models.CharField(max_length = 64)
    year = models.CharField(max_length = 64)
    genre = models.CharField(max_length = 64)
    rating = models.CharField(max_length = 64)
    status = models.CharField(max_length = 64)

class User(models.Model):
    username = models.CharField(max_length = 64,primary_key=True)
    password = models.CharField(max_length = 64)
    movies = models.ManyToManyField(movies, blank=True, related_name="watchers")


