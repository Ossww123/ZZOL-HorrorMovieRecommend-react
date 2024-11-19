# articles/serializers.py
from rest_framework import serializers
from .models import Article


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
