from django.db import models
from django.conf import settings
from accounts.models import User

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    adult = models.BooleanField()
    poster = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=None)
    # 여기 아래가 문제
    # cast는 배우 이름과 사진을 받아와야함
    # keywords는 외부에서 받아와야됨

class comment(models.Model):
    models.ForeignKey(User, on_delete=models.CASCADE)
    models.ForeignKey(Movie, on_delete=models.CASCADE)
    models.IntegerField()
    models.IntegerField()