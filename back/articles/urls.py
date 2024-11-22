# back/articles/urls.py
from django.urls import path
from . import views


urlpatterns = [
    path('articles/', views.article_list),
    path('articles/<int:article_pk>/', views.article_detail),
    path('movies/', views.save_movies_to_db),
    path('recommend/', views.recommend_movies, name='recommend_movies'),
    path('<int:movie_pk>/reviews/', views.review),
    path('<int:movie_pk>/reviews/<int:review_pk>/', views.review_update)
]
