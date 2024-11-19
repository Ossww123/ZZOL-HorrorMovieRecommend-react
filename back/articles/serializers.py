# articles/serializers.py
from rest_framework import serializers
from .models import Article
from rest_framework import serializers
from .models import Movie, Comment, Review


# 전체 영화 리스트 출력
class MovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

# 특정 영화 출력
class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

# 전체 리뷰 출력
class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

# 전체 댓글 출력
class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('user',)

    def create(self, validated_data):
        # 게시글을 저장할 때 현재 로그인한 사용자를 자동으로 저장
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('user',)
