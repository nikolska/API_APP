from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_list_or_404, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView , DetailView, FormView, ListView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView


from .forms import ArticleForm, ArticleSearchForm, CommentForm
from .models import Article, Comment
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    ArticleSerializer, ArticleCreateSerializer, ArticleDetailSerializer,  
    CommentSerializer, CommentCreateSerializer,
)


# Generic Views

class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'article_create.html'
    success_url = reverse_lazy('article_list')

    def form_valid(self, form):
        Article.objects.create(
            title=form.cleaned_data['title'],
            author=self.request.user,
            text=form.cleaned_data['text']
        )
        return HttpResponseRedirect(self.success_url)


class ArticleDetailView(DetailView, FormView):
    model = Article
    form_class = CommentForm
    template_name = 'article_detail.html'

    def get_context_data(self, **kwargs):
        comments = Comment.objects.filter(article=self.object)
        ctx = super().get_context_data(**kwargs)
        ctx['comments'] = comments
        return ctx
    
    def form_valid(self, form):
        Comment.objects.create(
            article=self.get_object(),
            author=self.request.user,
            comment_text=form.cleaned_data['comment_text']
        )
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))


class ArticleListView(ListView):
    model = Article
    template_name = 'home.html'


# API

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleCreateSerializer
    permission_classes = [IsAdminUser, IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['title', 'author__username', 'pub_date']
    search_fields = ['title', 'author__username']
    ordering_fields = ['title', 'author__username', 'pub_date']

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
    permission_classes = [IsAdminUser, IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

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
    permission_classes = [IsAdminUser, IsAuthenticated]

    def post(self, request, pk):
        comment = CommentCreateSerializer(data=request.data)
        if comment.is_valid():
            Comment.objects.create(
                author=request.user,
                article=get_object_or_404(Article, pk=pk),
                comment_text=comment.data['comment_text']
            )
        return HttpResponseRedirect(reverse('article-detail', args=(pk,)))

