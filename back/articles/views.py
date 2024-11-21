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
from .models import Article, Movie, Director, Actor, Comment, Review
from .serializers import ArticleListSerializer, ArticleSerializer, MovieListSerializer, MovieSerializer, ReviewSerializer, CommentSerializer

# TMDB API 설정
TMDB_API_URL = 'https://api.themoviedb.org/3'
TMDB_API_KEY = settings.TMDB_API_KEY


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def article_list(request):
    """
    게시글 목록 조회 (GET) 또는 게시글 생성 (POST)
    """
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
    """
    특정 게시글 상세 조회
    """
    article = get_object_or_404(Article, pk=article_pk)
    serializer = ArticleSerializer(article)
    print(serializer.data)
    return Response(serializer.data)


def fetch_movies_from_tmdb(num):
    """
    TMDB에서 영화 목록 가져오기 (장르: 공포, 페이지 번호: num)
    """
    url = f'{TMDB_API_URL}/discover/movie?api_key={TMDB_API_KEY}&with_genres=27&language=ko-KR&page={num}'
    response = requests.get(url)
    return response.json().get('results', []) if response.status_code == 200 else []


def fetch_movie_credits(movie_id):
    """
    TMDB에서 특정 영화의 출연진 정보 가져오기
    """
    url = f'{TMDB_API_URL}/movie/{movie_id}/credits?api_key={TMDB_API_KEY}&language=ko-KR'
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None


@api_view(['GET', 'POST'])
def save_movies_to_db(request):
    """
    TMDB에서 영화 데이터를 가져와 데이터베이스에 저장
    """
    if request.method == 'GET':
        movies = get_list_or_404(Movie)
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        for num in range(1, 10):
            print(num)
            movies_data = fetch_movies_from_tmdb(num)

            for movie_data in movies_data:
                print(movie_data)
                release_date = movie_data.get('release_date', '0001-01-01') or '0001-01-01'

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
                        'user_vote_cnt': 0,
                        'fear_index': 0,
                    }
                )

                # 영화 크레딧 데이터 저장
                credits = fetch_movie_credits(movie_data['id'])
                if credits:
                    directors = [crew for crew in credits.get('crew', []) if crew['job'] == 'Director']
                    for director_data in directors:
                        pp(director_data)
                        director, _ = Director.objects.get_or_create(
                            name=director_data['name'],
                            original_name=director_data.get('original_name', director_data['name']),
                            profile_path=director_data['profile_path']
                        )
                        print(movie.title, director.name)
                        movie.movie_director.add(director)

                    # 상위 5명의 배우 저장
                    actors = credits.get('cast', [])[:5]
                    for actor_data in actors:
                        print(actor_data)
                        actor, _ = Actor.objects.get_or_create(
                            name=actor_data['name'],
                            original_name=actor_data.get('original_name', actor_data['name']),
                            profile_path=actor_data['profile_path']
                        )
                        print(actor.name)
                        print('------------------------------')
                        movie.movie_actor.add(actor)
                    movie.save()


@api_view(['GET'])
def movie_detail(request, movie_pk):
    """
    특정 영화 상세 조회
    """
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = MovieSerializer(movie)
    print(serializer.data)
    return Response(serializer.data)


client = OpenAI(api_key=settings.OPENAI_API_KEY)


@csrf_exempt
def recommend_movies(request):
    """
    사용자 입력을 바탕으로 OpenAI와 TMDB API를 사용해 영화 추천
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_input = data.get('user_input')
            print(user_input)

            # OpenAI API를 사용해 키워드 추출
            keywords = extract_keywords(user_input)
            print('Extracted Keywords:', keywords)

            # TMDB API를 사용해 영화 추천
            allowed_genres = [
                "horror", "thriller", "action", "adventure", 
                "animation", "comedy", "crime", "documentary", "drama"
            ]
            movies = get_movies_by_keywords(keywords, allowed_genres)
            print(keywords, 'Movies:', movies)
            return JsonResponse({"movies": movies})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid method"}, status=400)


def extract_keywords(user_input):
    """
    사용자 입력에서 영화 관련 키워드 추출
    """
    try:
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
        keywords = response.choices[0].message.content.strip()
        try:
            return eval(keywords)
        except:
            print("Failed to parse keywords. Response was:", keywords)
            return []

    except Exception as e:
        print(f"Error in extract_keywords: {str(e)}")
        return []


def get_genre_ids():
    """
    TMDB에서 장르 ID를 가져오기
    """
    genre_url = f"{TMDB_API_URL}/genre/movie/list?api_key={TMDB_API_KEY}&language=en-US"
    response = requests.get(genre_url).json()
    return {genre['name'].lower(): genre['id'] for genre in response.get('genres', [])}


def get_movies_by_keywords(keywords, allowed_genres):
    """
    키워드와 허용된 장르를 사용해 TMDB에서 영화 추천
    """
    genre_ids = get_genre_ids()
    allowed_genre_ids = {genre_ids[genre] for genre in allowed_genres if genre in genre_ids}

    movie_list = []
    for keyword in keywords:
        search_url = f"{TMDB_API_URL}/search/keyword?api_key={TMDB_API_KEY}&query={keyword}"
        response = requests.get(search_url).json()
        if response.get("results"):
            keyword_id = response["results"][0]["id"]
            movies_url = f"{TMDB_API_URL}/keyword/{keyword_id}/movies?api_key={TMDB_API_KEY}"
            movies_response = requests.get(movies_url).json()
            movie_list.extend(movies_response.get("results", []))

    unique_movies = {movie['id']: movie for movie in movie_list}.values()
    filtered_movies = [
        movie for movie in unique_movies
        if any(genre_id in allowed_genre_ids for genre_id in movie.get('genre_ids', []))
    ]

    return sorted(filtered_movies, key=lambda x: x.get('popularity', 0), reverse=True)[:5]


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def review(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)

    if Review.objects.filter(user=request.user, movie=movie).exists():
        return Response({'error' : '나가 임마'}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user, movie=movie)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
@permission_classes([IsAuthenticated])
def review_detail(request, movie_pk, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    
    # 리뷰 작성자만 수정/삭제 가능
    if review.user != request.user:
        return Response({'error': '니가 뭔데'}, 
                      status=status.HTTP_403_FORBIDDEN)

    if request.method == 'PUT':
        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)

    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user, movie=movie)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def comment_detail(request, movie_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    
    # 리뷰 작성자만 수정/삭제 가능
    if comment.user != request.user:
        return Response({'error': '니가 뭔데'}, 
                      status=status.HTTP_403_FORBIDDEN)

    if request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    elif request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)