from django.http import HttpResponseRedirect
from django.shortcuts import get_list_or_404, get_object_or_404
from django.urls import reverse
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Article, Comment
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    ArticleSerializer, ArticleCreateSerializer, ArticleDetailSerializer,  
    CommentSerializer, CommentCreateSerializer,
)


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = get_list_or_404(Article)
    serializer_class = ArticleCreateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def list(self, request):
        articles = self.queryset
        serializer = ArticleSerializer(articles, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        serializer = ArticleDetailSerializer(article, many=False, context={'request': request})
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = get_list_or_404(Comment)
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def list(self, request):
        comments = self.queryset
        serializer = self.serializer_class(comments, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        serializer = self.serializer_class(comment, many=False, context={'request': request})
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        comment = CommentCreateSerializer(data=request.data)
        if comment.is_valid():
            Comment.objects.create(
                author=request.user,
                article=get_object_or_404(Article, pk=pk),
                comment_text=comment.data['comment_text']
            )
        return HttpResponseRedirect(reverse('article-detail', args=(pk,)))

