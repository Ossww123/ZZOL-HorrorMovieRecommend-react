# articles/views.py

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

# permission Decorators
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404, get_list_or_404

from .serializers import ArticleListSerializer, ArticleSerializer, MovieListSerializer
from .models import Article


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def article_list(request):
    if request.method == 'GET':
        articles = get_list_or_404(Article)
        serializer = ArticleListSerializer(articles, many=True)
        pp(serializer.data)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # serializer.save()
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def article_detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        print(serializer.data)
        return Response(serializer.data)




from django.shortcuts import render, get_list_or_404, get_object_or_404
import requests
from django.conf import settings
from .models import Movie
from pprint import pprint as pp


# Create your views here.
TMDB_API_URL = 'https://api.themoviedb.org/3'
TMDB_API_KEY = '662d994d5646c21b0c76646bc0adfcb6'

# 영화 목록을 TMDb에서 가져오는 함수
def fetch_movies_from_tmdb():
    url = f'{TMDB_API_URL}/movie/popular?api_key={TMDB_API_KEY}&language=ko-KR&page=5'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('results', [])
    return []


# pp(fetch_movies_from_tmdb())


@api_view(['GET', 'POST'])
def save_movies_to_db(request):
    movies_data = fetch_movies_from_tmdb()
    
    if request.method == 'GET':
        movies = get_list_or_404(Movie)
        serializer = MovieListSerializer(movies, many=True)
        pp(serializer.data)
        return Response(serializer.data)




    if request.method == 'POST':
        for movie_data in movies_data:
            # 영화 데이터 저장
            movie, created = Movie.objects.get_or_create(
                tmdb_Id=movie_data['id'],
                defaults={
                    'title': movie_data['title'],
                    'original_title': movie_data['original_title'],
                    'release_date': movie_data['release_date'],
                    'popularity': movie_data['popularity'],
                    'tmdb_vote_sum': movie_data['vote_average'],
                    'tmdb_vote_cnt': movie_data['vote_count'],
                    'overview': movie_data['overview'],
                    'poster_path': movie_data['poster_path'],
                    'backdrop_path': movie_data['backdrop_path'],
                    'adult': movie_data['adult'],
                    'user_vote_sum': 0,
                    'user_vote_cnt' : 0,
                    'fear_index': 0,
                }
            )

            # # 감독 정보 저장 (예시로 하나의 감독만 처리)
            # for director_data in movie_data.get('directors', []):
            #     director, _ = Director.objects.get_or_create(
            #         name=director_data['name'],
            #         original_name=director_data['original_name']
            #     )
            #     movie.movie_director.add(director)

            # # 배우 정보 저장 (예시로 하나의 배우만 처리)
            # for actor_data in movie_data.get('actors', []):
            #     actor, _ = Actor.objects.get_or_create(
            #         name=actor_data['name'],
            #         original_name=actor_data['original_name']
            #     )
            #     movie.movie_actor.add(actor)

            # 영화와 감독/배우 관계 저장
            movie.save()