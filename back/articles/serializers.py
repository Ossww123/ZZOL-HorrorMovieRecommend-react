# articles/serializers.py
from rest_framework import serializers
from .models import Article
from rest_framework import serializers
from .models import Movie, Comment, Review, ArticleComment
from django.contrib.auth import get_user_model

# User 시리얼라이저
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()  # 커스터마이징한 User 모델을 사용
        fields = '__all__'  # 원하는 필드만 포함 (nickname)

# 전체 영화 리스트 출력
class MovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

# 특정 영화 출력
class MovieSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = '__all__'

    def get_average_rating(self, obj):
        return obj.get_average_rating()

    def get_review_count(self, obj):
        return obj.user_vote_cnt
    
# 전체 리뷰 출력
class ReviewListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # user 정보도 포함되도록 설정
    
    class Meta:
        model = Review
        fields = '__all__'

#리뷰 출력
class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # user 정보도 포함되도록 설정

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('user', 'movie', 'created_at', 'updated_at')

# 전체 댓글 출력
class CommentListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('user', )
    
    def get_user(self, obj):
        return {
            'id': obj.user.id,
            'nickname': obj.user.nickname
        }

class CommentSerializer(serializers.ModelSerializer):
    user_nickname = serializers.CharField(source='user.nickname', read_only=True)
    
    class Meta:
        model = Comment
        fields = ('content', 'user_nickname', )
        read_only_fields = ('user', )


class ArticleCommentListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = ArticleComment
        fields = '__all__'
        read_only_fields = ('user', )
    
    def get_user(self, obj):
        return {
            'id': obj.user.id,
            'nickname': obj.user.nickname
        }

class ArticleCommentSerializer(serializers.ModelSerializer):
    user_nickname = serializers.CharField(source='user.nickname', read_only=True)
    
    class Meta:
        model = ArticleComment
        fields = ('content', 'user_nickname', )
        read_only_fields = ('user', )




class ArticleListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('user', 'recommend_users')

    def create(self, validated_data):
        # 게시글을 저장할 때 현재 로그인한 사용자를 자동으로 저장
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class ArticleSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('user', 'recommend_users')