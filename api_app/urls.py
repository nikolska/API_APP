from django.urls import path

from .views import (
    #Generic Views
    ArticleCreateView, ArticleDetailView, ArticleListView, 
    
    # API Views
    ArticleViewSet, CommentViewSet, CommentCreateAPIView
)


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
    path('', ArticleListView.as_view(), name='article_list'),
    path('article/new/', ArticleCreateView.as_view(), name='article_create'),
    path('article/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    # API
    path('api/articles/', article_list, name='article-list'),
    path('api/articles/<int:pk>/', article_detail, name='article-detail'),
    path('api/comments/', comment_list, name='comment-list'),
    path('api/comments/new/<int:pk>/', CommentCreateAPIView.as_view(), name='add-new-comment'),
    path('api/comments/<int:pk>/', comment_detail, name='comment-detail'),
]

