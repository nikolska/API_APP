from django.contrib.auth.models import Group, User
from rest_framework import serializers


from .models import Article, Comment


class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Article
        fields = ['title', 'author', 'pub_date']


class CommentSerializer(serializers.ModelSerializer):
    article = serializers.SlugRelatedField(slug_field='title', read_only=True)
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = ['article', 'author', 'pub_date']

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['article', 'author', 'comment_text', 'pub_date']


class CommentDetailSerializer(serializers.ModelSerializer):
    article = serializers.SlugRelatedField(slug_field='title', read_only=True)
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)
    
    class Meta:
        model = Comment
        fields = ['article', 'author', 'comment_text', 'pub_date']


class ArticleDetailSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)
    comments = CommentDetailSerializer(many=True)

    class Meta:
        model = Article
        fields = ['title', 'author', 'text', 'pub_date', 'comments']
