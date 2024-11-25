# back/articles/urls.py
from django.urls import path
from . import views


urlpatterns = [
    path('articles/', views.article_list),
    path('articles/<int:article_pk>/', views.article_detail),
    path('movies/<int:movie_pk>/', views.movie_detail),
    # 영화 출력 및 데이터 생성 경로
    path('movies/', views.save_movies_to_db),
    # 감독
    path('directors/<int:director_pk>/', views.director_info),
    path('actors/<int:actor_pk>/', views.actor_info),
    # 추천
    path('recommend/', views.recommend_movies, name='recommend_movies'),
    path('movielist/', views.movie_list),
    path('random/', views.random_movie),
    path('random/<int:tmdb_id>/', views.random_detail),
    # 리뷰 경로
    path('<int:movie_pk>/reviews/', views.review),
    path('<int:movie_pk>/reviews/<int:review_pk>/', views.review_update),
    path('random/<int:tmdb_id>/reviews/', views.random_review),
    path('random/<int:tmdb_id>/reviews/<int:review_pk>/', views.random_review_update),
    # 댓글 경로
    path('<int:review_pk>/comments/', views.comment),
    path('<int:review_pk>/comments/<int:comment_pk>/', views.comment_update),
]