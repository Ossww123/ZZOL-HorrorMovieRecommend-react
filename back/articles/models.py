# articles/models.py
from django.db import models
from django.conf import settings
from platform import release
from tkinter import CASCADE
from django.db import models
from django.conf import settings

# Create your models here.
class Director(models.Model):
    name = models.CharField(max_length=200)
    original_name = models.CharField(max_length=200)

class Actor(models.Model):
    name = models.CharField(max_length=200)
    original_name = models.CharField(max_length=200)

class Movie(models.Model):
    tmdb_Id = models.IntegerField()
    title = models.CharField(max_length=200)
    original_title = models.CharField(max_length=200)
    release_date = models.DateTimeField()
    popularity = models.FloatField()
    tmdb_vote_sum = models.FloatField()
    tmdb_vote_cnt = models.IntegerField()
    user_vote_sum = models.IntegerField()
    user_vote_cnt = models.IntegerField()
    fear_index = models.IntegerField()
    overview = models.TextField()
    poster_path = models.TextField() 
    backdrop_path = models.TextField()
    adult = models.BooleanField()
    movie_director = models.ManyToManyField(Director)
    movie_actor = models.ManyToManyField(Actor)

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rate = models.IntegerField()
    fear_score = models.IntegerField()

    
    
class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Article(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
