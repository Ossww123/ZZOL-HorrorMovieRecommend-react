# articles/models.py
from django.db import models
from django.conf import settings
from django.db import models
from django.conf import settings

# Create your models here.
class Director(models.Model):
    name = models.CharField(max_length=200)
    original_name = models.CharField(max_length=200)
    profile_path = models.TextField(blank=True, null=True) 

class Actor(models.Model):
    name = models.CharField(max_length=200)
    original_name = models.CharField(max_length=200)
    profile_path = models.TextField(blank=True, null=True)

class Movie(models.Model):
    tmdb_Id = models.IntegerField()
    title = models.CharField(max_length=200)
    original_title = models.CharField(max_length=200)
    release_date = models.DateField(blank=True, null=True)
    popularity = models.FloatField()
    tmdb_vote_sum = models.FloatField()
    tmdb_vote_cnt = models.IntegerField()
    user_vote_sum = models.FloatField()
    user_vote_cnt = models.IntegerField()
    fear_index = models.IntegerField()
    overview = models.TextField(blank=True, null=True)
    poster_path = models.TextField(blank=True, null=True) 
    backdrop_path = models.TextField(blank=True, null=True)
    adult = models.CharField(max_length=50)
    movie_director = models.ManyToManyField(Director)
    movie_actor = models.ManyToManyField(Actor)

    def update_ratings(self):
        # """리뷰를 기반으로 평점과 공포 지수 업데이트"""
        reviews = self.review_set.all()
        
        if reviews.exists():
            # 평점 관련 데이터 업데이트
            self.user_vote_cnt = reviews.count()
            vote_sum = sum(review.rate for review in reviews)
            self.user_vote_sum = round(vote_sum / self.user_vote_cnt, 1)
            
            # 공포 지수 업데이트
            total_fear = sum(review.fear_score for review in reviews)
            self.fear_index = total_fear // self.user_vote_cnt
        else:
            # 리뷰가 없는 경우 초기화
            self.user_vote_cnt = 0
            self.user_vote_sum = 0
            self.fear_index = 0
        
        self.save()

    def get_average_rating(self):
        # """평균 평점 계산"""
        if self.user_vote_cnt > 0:
            return round(self.user_vote_sum / self.user_vote_cnt, 1)
        return 0

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rate = models.IntegerField()
    fear_score = models.IntegerField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.movie.update_ratings()

    def delete(self, *args, **kwargs):
        movie = self.movie
        super().delete(*args, **kwargs)
        movie.update_ratings()
    
class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Article(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    recommend_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='recommend_articles')
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ArticleComment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)