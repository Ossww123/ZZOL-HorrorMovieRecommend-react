# back/articles/views.py
import random
import json
from django.db.models import Count
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
from .models import Article, Movie, Director, Actor, Comment, Review, ArticleComment
from .serializers import ArticleListSerializer, ArticleSerializer, CommentListSerializer, MovieListSerializer, MovieSerializer, ReviewSerializer, CommentSerializer, ArticleCommentListSerializer, ArticleCommentSerializer

# TMDB API 설정
TMDB_API_URL = 'https://api.themoviedb.org/3'
TMDB_API_KEY = settings.TMDB_API_KEY

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def check_spoiler(content):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "영화 리뷰의 스포일러 여부를 판단하는 AI입니다. 스포일러가 있으면 True, 없으면 False를 반환하세요."
                },
                {
                    "role": "user",
                    "content": f"다음 리뷰가 스포일러를 포함하고 있는지 True/False로만 답변하세요: {content}"
                }
            ],
            max_tokens=10,
            temperature=0.3
        )
        return response.choices[0].message.content.strip().lower() == 'true'
    except Exception as e:
        print(f"스포일러 체크 오류: {str(e)}")
        return False


def check_inappropriate_content(content):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "댓글의 욕설이나 혐오발언 여부를 판단하는 AI입니다. 부적절한 내용이 있으면 True, 없으면 False를 반환하세요."
                },
                {
                    "role": "user",
                    "content": f"다음 댓글이 욕설이나 혐오발언을 포함하고 있는지 True/False로만 답변하세요: {content}"
                }
            ],
            max_tokens=10,
            temperature=0.3
        )
        return response.choices[0].message.content.strip().lower() == 'true'
    except Exception as e:
        print(f"부적절 내용 체크 오류: {str(e)}")
        return False



@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def article_list(request):
    """
    게시글 목록 조회 (GET) 또는 게시글 생성 (POST)
    """
    if request.method == 'GET':
        articles = Article.objects.all()
        top_articles = articles.annotate(
        recommend_count=Count('recommend_users')
        ).order_by('-recommend_count')[:5]
        
        # 나머지 게시글 최신순 정렬 (상위 5개 제외)
        remaining_articles = articles.exclude(
            id__in=top_articles.values_list('id', flat=True)
        ).order_by('-created_at')
        
        # 두 쿼리셋 합치기
        serializer_top = ArticleListSerializer(top_articles, many=True)
        serializer_remaining = ArticleListSerializer(remaining_articles, many=True)
        
        return Response({
            'top_articles': serializer_top.data,
            'remaining_articles': serializer_remaining.data
        })

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


from .serializers import ReviewListSerializer

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def review(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.method == 'GET':
        reviews = Review.objects.filter(movie=movie)
        serializer = ReviewListSerializer(reviews, many=True)
        pp(serializer.data)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        if Review.objects.filter(user=request.user, movie=movie).exists():
            return Response({'error' : '나가 임마'}, status=status.HTTP_400_BAD_REQUEST)
        
        if check_spoiler(request.data['content']):
            return Response({'error': '스포일러가 포함된 리뷰는 작성할 수 없습니다'}, 
                       status=status.HTTP_400_BAD_REQUEST)

        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, movie=movie)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['PUT', 'DELETE'])    
@permission_classes([IsAuthenticated])
def review_update(request, movie_pk, review_pk):
    review = Review.objects.get(pk=review_pk)
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

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def comment(request, review_pk):
    # 1개의 리뷰에 댓글이 달릴거니까 가져오고
    review = get_object_or_404(Review, pk=review_pk)
    # get이면 리뷰에 달린 댓글을 출력합니다.
    if request.method == 'GET':
        comments = Comment.objects.filter(review=review)
        serializer = CommentListSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    # post면 리뷰에 댓글을 생성합니다.
    elif request.method == 'POST':
        if check_inappropriate_content(request.data['content']):
            return Response({'error': '부적절한 내용이 포함된 댓글은 작성할 수 없습니다'}, 
                       status=status.HTTP_400_BAD_REQUEST)


        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, review=review)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def comment_update(request, review_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    
    # 리뷰 작성자만 수정/삭제 가능
    if comment.user != request.user:
        return Response({'error': '니가 뭔데 여길 와'}, 
                      status=status.HTTP_403_FORBIDDEN)

    if request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    elif request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
# 항목에 따른 정렬 함수
def movie_list(request):
    sort_by = request.query_params.get('sort', 'popularity')
    if sort_by == 'popularity':
        movies = Movie.objects.all().order_by('-popularity')[:5]
    elif sort_by == 'latest':
        movies = Movie.objects.all().order_by('-release_date')[:5]
    elif sort_by == 'rating':
        movies = Movie.objects.all().order_by('-tmdb_vote_sum')[:5]
    elif sort_by == 'fear':
        movies = Movie.objects.all().order_by('-fear_index')[:5]
    
    serializer = MovieListSerializer(movies, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def random_movie(request):
    horror_keywords = {
        'possession': {'id': 178646, 'name': '악령 포제션'},
        'serial killer': {'id': 9663, 'name': '연쇄 살인'},
        'supernatural': {'id': 6152, 'name': '초자연현상'},
        'monster': {'id': 1299, 'name': '괴물/크리처'},
        'isolation': {'id': 1533, 'name': '고립된 공간'},
        'zombie': {'id': 12377, 'name': '좀비'},
        'dark secret': {'id': 10349, 'name': '가족의 비밀'},
        'ritual': {'id': 4720, 'name': '의식/제의'},
        'survival': {'id': 10349, 'name': '생존 공포'},
        'psychological horror': {'id': 295907, 'name': '정신적 공포'}
    }
    
    selected_keywords = random.sample(list(horror_keywords.keys()), 2)
    results = {}
    
    for keyword in selected_keywords:
        params = {
            'api_key': settings.TMDB_API_KEY,
            'with_keywords': horror_keywords[keyword]['id'],
            'sort_by': 'popularity.desc',
            'with_genres': 27,
            'language': 'ko-KR'
        }
        
        response = requests.get('https://api.themoviedb.org/3/discover/movie', params=params)
        movies = response.json()['results'][:8]
        results[horror_keywords[keyword]['name']] = movies
    return Response(results)


@api_view(['GET'])
def random_detail(request, tmdb_id):
    try:
        # DB에서 영화 검색
        movie = Movie.objects.get(tmdb_Id=tmdb_id)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)
    except Movie.DoesNotExist:
        # DB에 없는 경우 TMDB에서 영화 정보 가져오기
        url = f'{TMDB_API_URL}/movie/{tmdb_id}?api_key={TMDB_API_KEY}&language=ko-KR'
        movie_data = requests.get(url).json()
        
        # 영화 데이터 저장
        movie = Movie.objects.create(
            tmdb_Id=tmdb_id,
            title=movie_data['title'],
            original_title=movie_data['original_title'],
            release_date=movie_data.get('release_date', '0001-01-01'),
            popularity=movie_data['popularity'],
            tmdb_vote_sum=movie_data['vote_average'],
            tmdb_vote_cnt=movie_data['vote_count'],
            overview=movie_data['overview'],
            poster_path=movie_data['poster_path'],
            backdrop_path=movie_data['backdrop_path'],
            adult=movie_data['adult'],
            user_vote_sum=0,
            user_vote_cnt=0,
            fear_index=0
        )
        
        # 감독과 배우 정보 저장
        credits = fetch_movie_credits(tmdb_id)
        if credits:
            # 감독 정보 저장
            directors = [crew for crew in credits.get('crew', []) if crew['job'] == 'Director']
            for director_data in directors:
                director, _ = Director.objects.get_or_create(
                    name=director_data['name'],
                    original_name=director_data.get('original_name', director_data['name']),
                    profile_path=director_data['profile_path']
                )
                movie.movie_director.add(director)
            
            # 배우 정보 저장 (상위 5명)
            actors = credits.get('cast', [])[:5]
            for actor_data in actors:
                actor, _ = Actor.objects.get_or_create(
                    name=actor_data['name'],
                    original_name=actor_data.get('original_name', actor_data['name']),
                    profile_path=actor_data['profile_path']
                )
                movie.movie_actor.add(actor)
        
        serializer = MovieSerializer(movie)
        return Response(serializer.data)
    

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def random_review(request, tmdb_id):
    movie = get_object_or_404(Movie, tmdb_Id=tmdb_id)
    if request.method == 'GET':
        reviews = Review.objects.filter(movie=movie)
        serializer = ReviewListSerializer(reviews, many=True)
        pp(serializer.data)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        if Review.objects.filter(user=request.user, movie=movie).exists():
            return Response({'error' : '나가 임마'}, status=status.HTTP_400_BAD_REQUEST)
        
        if check_spoiler(request.data['content']):
            return Response({'error': '스포일러가 포함된 리뷰는 작성할 수 없습니다'}, 
                       status=status.HTTP_400_BAD_REQUEST)

        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, movie=movie)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PUT', 'DELETE'])    
@permission_classes([IsAuthenticated])
def random_review_update(request, tmdb_id, review_pk):
    review = Review.objects.get(pk=review_pk)
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
    

@api_view(['GET'])
def director_info(request, director_pk):
    director = get_object_or_404(Director, pk=director_pk)
    return Response({
        'name': director.name,
        'original_name': director.original_name,
        'profile_path': director.profile_path
    })

@api_view(['GET'])
def actor_info(request, actor_pk):
    actor = get_object_or_404(Actor, pk=actor_pk)
    return Response({
        'name': actor.name,
        'original_name': actor.original_name,
        'profile_path': actor.profile_path
    })


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def article_comments(request, article_id):
    # 1개의 리뷰에 댓글이 달릴거니까 가져오고
    article = get_object_or_404(Article, id=article_id)
    # get이면 리뷰에 달린 댓글을 출력합니다.
    if request.method == 'GET':
        comments = ArticleComment.objects.filter(article=article)
        serializer = ArticleCommentListSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    # post면 리뷰에 댓글을 생성합니다.
    elif request.method == 'POST':
        if check_inappropriate_content(request.data['content']):
            return Response({'error': '부적절한 내용이 포함된 댓글은 작성할 수 없습니다'}, 
                       status=status.HTTP_400_BAD_REQUEST)


        serializer = ArticleCommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, article=article)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def article_comment_update(request, article_id, comment_pk):
    comment = get_object_or_404(ArticleComment, pk=comment_pk)
    
    # 댓글 작성자만 수정/삭제 가능
    if comment.user != request.user:
        return Response({'error': '니가 뭔데 여길 와'}, 
                      status=status.HTTP_403_FORBIDDEN)

    if request.method == 'PUT':
        serializer = ArticleCommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    elif request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def recommends(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    if request.user in article.recommend_users.all():
        article.recommend_users.remove(request.user)
        is_recommended = False
    else:
        article.recommend_users.add(request.user)
        is_recommended = True
    
    return Response({
        'is_recommended': is_recommended,
        'recommend_count': article.recommend_users.count()
    })