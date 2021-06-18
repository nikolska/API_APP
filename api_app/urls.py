from django.urls import path
from django.urls.resolvers import URLPattern

from .views import (
    ArticleDetailView, ArticleListView,
    CommentCreateView, CommentDetailView, CommentListView
)

urlpatterns = [
    path('articles/', ArticleListView.as_view()),
    path('articles/<int:pk>/', ArticleDetailView.as_view()),
    path('comments/', CommentListView.as_view()),
    path('comments/<int:pk>/', CommentDetailView.as_view()),
    path('comments/create-new/', CommentCreateView.as_view()),
]

