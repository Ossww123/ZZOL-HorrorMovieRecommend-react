# back/articles/views.py

import json
import requests
from pprint import pprint as pp
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.conf import settings
from django.shortcuts import get_object_or_404, get_list_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from openai import OpenAI
from .models import Article, Movie, Director, Actor
from .serializers import ArticleListSerializer, ArticleSerializer, MovieListSerializer, MovieSerializer





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
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def article_detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        print(serializer.data)
        return Response(serializer.data)





# Create your views here.
TMDB_API_URL = 'https://api.themoviedb.org/3'
TMDB_API_KEY = settings.TMDB_API_KEY

# 영화 목록을 TMDb에서 가져오는 함수
def fetch_movies_from_tmdb(num):
    # url = f'{TMDB_API_URL}/movie/popular?api_key={TMDB_API_KEY}&language=ko-KR&page={num}'
    url = f'https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&with_genres=27&language=ko-KR&page={num}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('results', [])
    return []

def fetch_movie_credits(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={TMDB_API_KEY}&language=ko-KR'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

@api_view(['GET', 'POST'])
def save_movies_to_db(request):
    
    if request.method == 'GET':
        movies_data = fetch_movies_from_tmdb()
        movies = get_list_or_404(Movie)
        serializer = MovieListSerializer(movies, many=True)
        # pp(serializer.data)
        return Response(serializer.data)




    if request.method == 'POST':
        for num in range(1, 10):
            print(num)
            movies_data = fetch_movies_from_tmdb(num)
            for movie_data in movies_data:
                print(movie_data)
                release_date = movie_data.get('release_date', None)
            
                # 날짜가 빈 문자열이면 None으로 처리
                if release_date == "":
                    release_date = '0001-01-01'
            
                # 영화 데이터 저장
                movie, created = Movie.objects.get_or_create(
                    tmdb_Id=movie_data['id'],
                    defaults={
                        'title': movie_data['title'],
                        'original_title': movie_data['original_title'],
                        'release_date': release_date,
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


                credits = fetch_movie_credits(movie_data['id'])
                if credits:
                    # 감독 정보 저장 (예시로 하나의 감독만 처리)
                    directors = [crew for crew in credits.get('crew', []) if crew['job'] == 'Director']
                    for director_data in directors:
                        pp(director_data)
                        director, _ = Director.objects.get_or_create(
                            name=director_data['name'],
                            original_name=director_data.get('original_name', director_data['name']),
                            profile_path=director_data['profile_path'],
                            # known_for=director_data['known_for'],
                        )
                        print(movie.title)
                        print(director.name)
                        movie.movie_director.add(director)

                    # 배우 정보 저장 (상위 5명만)
                    actors = credits.get('cast', [])[:5]
                    for actor_data in actors:
                        print(actor_data)
                        actor, _ = Actor.objects.get_or_create(
                            name=actor_data['name'],
                            original_name=actor_data.get('original_name', actor_data['name']),
                            profile_path=actor_data['profile_path'],
                            # known_for=actor_data['credit'],
                        )
                        
                        print(actor.name)
                        print('------------------------------')
                        movie.movie_actor.add(actor)
                    # 영화와 감독/배우 관계 저장
                    movie.save()

@api_view(['GET'])
def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)

    if request.method == 'GET':
        serializer = MovieSerializer(movie)
        print(serializer.data)
        return Response(serializer.data)
    



client = OpenAI(api_key=settings.OPENAI_API_KEY)

@csrf_exempt
def recommend_movies(request):
    if request.method == "POST":
        try:
            # 클라이언트로부터 입력 받은 데이터
            data = json.loads(request.body)
            user_input = data.get('user_input')
            print(user_input)

            # OpenAI API 호출: 키워드 추출
            keywords = extract_keywords(user_input)

            print('              aaaaaaaaaaaa              ', keywords)

            # TMDB API 호출: 키워드를 기반으로 영화 추천

            allowed_genres = ["horror", "thriller", "action", "adventure", "animation", "comedy", "crime", "documentary", "drama"]


            movies = get_movies_by_keywords(keywords, allowed_genres)

            print(keywords, '               ', movies)

            return JsonResponse({"movies": movies})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid method"}, status=400)

# OpenAI API에서 영화 관련 키워드를 추출하는 함수
def extract_keywords(user_input):
    try:
        # 새로운 OpenAI API 호출 방식
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                "role": "system",
                "content": (
                    "You are a helpful assistant that extracts movie-related keywords "
                    "from user input in a specific format. Your task is to ensure the keywords "
                    "align with those found in the TMDB database. Return the keywords in the following format:\n\n"
                    "[\"keyword1\", \"keyword2\", \"keyword3\"]"
                )
            },
            {
                "role": "user",
                "content": (
                    f"Extract the three most relevant TMDB movie-related keywords from this input: \"{user_input}\". "
                    "Return the keywords as a Python list, using double quotes for each keyword."
                )
            }
            ],
            max_tokens=50,
            temperature=0.7
        )
        
        # 새로운 응답 구조에 맞게 데이터 추출
        keywords = response.choices[0].message.content.strip()
        try:
            return eval(keywords)
        except:
            print("Failed to parse keywords. Response was:", keywords)
            return []
            
    except Exception as e:
        print(f"Error in extract_keywords: {str(e)}")
        return []
    

BASE_URL = "https://api.themoviedb.org/3"

def get_genre_ids():
    genre_url = f"{BASE_URL}/genre/movie/list?api_key={TMDB_API_KEY}&language=en-US"
    response = requests.get(genre_url).json()
    return {genre['name'].lower(): genre['id'] for genre in response.get('genres', [])}


# TMDB API에서 키워드를 기반으로 영화 리스트를 가져오는 함수
def get_movies_by_keywords(keywords, allowed_genres):
    genre_ids = get_genre_ids()  # Fetch genre IDs
    allowed_genre_ids = {genre_ids[genre] for genre in allowed_genres if genre in genre_ids}

    movie_list = []
    for keyword in keywords:
        search_url = f"{BASE_URL}/search/keyword?api_key={TMDB_API_KEY}&query={keyword}"
        response = requests.get(search_url).json()
        if response.get("results"):
            keyword_id = response["results"][0]["id"]
            movies_url = f"{BASE_URL}/keyword/{keyword_id}/movies?api_key={TMDB_API_KEY}"
            movies_response = requests.get(movies_url).json()
            movie_list.extend(movies_response.get("results", []))
    
    # Remove duplicates and filter by genre
    unique_movies = {movie['id']: movie for movie in movie_list}.values()
    filtered_movies = [
        movie for movie in unique_movies
        if any(genre_id in allowed_genre_ids for genre_id in movie.get('genre_ids', []))
    ]

    # Sort movies by popularity in descending order
    sorted_movies = sorted(filtered_movies, key=lambda x: x.get('popularity', 0), reverse=True)

    return sorted_movies[:5]  # Return top 5 movies


# -----------------------------------------------------------------------------------------------------------------------------------------
# articles/views.py

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
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def article_detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        print(serializer.data)
        return Response(serializer.data)





# Create your views here.
TMDB_API_URL = 'https://api.themoviedb.org/3'
TMDB_API_KEY = settings.TMDB_API_KEY

# 영화 목록을 TMDb에서 가져오는 함수
def fetch_movies_from_tmdb(num):
    # url = f'{TMDB_API_URL}/movie/popular?api_key={TMDB_API_KEY}&language=ko-KR&page={num}'
    url = f'https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&with_genres=27&language=ko-KR&page={num}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('results', [])
    return []

def fetch_movie_credits(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={TMDB_API_KEY}&language=ko-KR'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

@api_view(['GET', 'POST'])
def save_movies_to_db(request):
    
    if request.method == 'GET':
        movies_data = fetch_movies_from_tmdb()
        movies = get_list_or_404(Movie)
        serializer = MovieListSerializer(movies, many=True)
        # pp(serializer.data)
        return Response(serializer.data)




    if request.method == 'POST':
        for num in range(1, 2):
            print(num)
            movies_data = fetch_movies_from_tmdb(num)
            for movie_data in movies_data:
                print(movie_data)
                release_date = movie_data.get('release_date', None)
            
                # 날짜가 빈 문자열이면 None으로 처리
                if release_date == "":
                    release_date = '0001-01-01'
            
                # 영화 데이터 저장
                movie, created = Movie.objects.get_or_create(
                    tmdb_Id=movie_data['id'],
                    defaults={
                        'title': movie_data['title'],
                        'original_title': movie_data['original_title'],
                        'release_date': release_date,
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


                credits = fetch_movie_credits(movie_data['id'])
                if credits:
                    # 감독 정보 저장 (예시로 하나의 감독만 처리)
                    directors = [crew for crew in credits.get('crew', []) if crew['job'] == 'Director']
                    for director_data in directors:
                        pp(director_data)
                        director, _ = Director.objects.get_or_create(
                            name=director_data['name'],
                            original_name=director_data.get('original_name', director_data['name']),
                            profile_path=director_data['profile_path'],
                            # known_for=director_data['known_for'],
                        )
                        print(movie.title)
                        print(director.name)
                        movie.movie_director.add(director)

                    # 배우 정보 저장 (상위 5명만)
                    actors = credits.get('cast', [])[:5]
                    for actor_data in actors:
                        print(actor_data)
                        actor, _ = Actor.objects.get_or_create(
                            name=actor_data['name'],
                            original_name=actor_data.get('original_name', actor_data['name']),
                            profile_path=actor_data['profile_path'],
                            # known_for=actor_data['credit'],
                        )
                        
                        print(actor.name)
                        print('------------------------------')
                        movie.movie_actor.add(actor)
                    # 영화와 감독/배우 관계 저장
                    movie.save()

@api_view(['GET'])
def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)

    if request.method == 'GET':
        serializer = MovieSerializer(movie)
        print(serializer.data)
        return Response(serializer.data)