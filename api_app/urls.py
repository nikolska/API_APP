from django.urls import path
from django.urls.resolvers import URLPattern

from .views import ArticleViewSet, CommentViewSet, CommentCreateAPIView


article_list = ArticleViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

article_detail = ArticleViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
})

comment_list = CommentViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

comment_detail = CommentViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
})


urlpatterns = [
    path('articles/', article_list, name='article-list'),
    path('articles/<int:pk>/', article_detail, name='article-detail'),
    path('comments/', comment_list, name='comment-list'),
    path('comments/new/<int:pk>/', CommentCreateAPIView.as_view(), name='add-new-comment'),
    path('comments/<int:pk>/', comment_detail, name='comment-detail'),
]

