from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Article, Comment
from .serializers import (
    ArticleDetailSerializer, ArticleSerializer, 
    CommentCreateSerializer, CommentDetailSerializer, CommentSerializer, 
)


class ArticleDetailView(APIView):
    def get(self, request, pk):
        article = Article.objects.get(pk=pk)
        serializer = ArticleDetailSerializer(article)
        return Response(serializer.data)


class ArticleListView(APIView):
    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)


class CommentCreateView(APIView):    
    def post(self, request):
        comment = CommentCreateSerializer(data=request.data)
        if comment.is_valid():
            comment.save()
        return Response(status=201)


class CommentDetailView(APIView):
    def get(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        serializer = CommentDetailSerializer(comment)
        return Response(serializer.data)


class CommentListView(APIView):
    def get(self, request):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

