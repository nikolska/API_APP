from rest_framework import serializers

from .models import Article, Comment


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Article
        fields = ['url', 'title', 'author', 'pub_date']


class ArticleCreateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Article
        fields = ['title', 'text']


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    article = serializers.SlugRelatedField(slug_field='title', read_only=False, queryset=Article.objects.all())
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)
    
    class Meta:
        model = Comment
        fields = ['url', 'article', 'author', 'comment_text', 'pub_date']


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['comment_text',]


class ArticleDetailSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)
    comments = CommentSerializer(many=True)
    add_new_comment = serializers.HyperlinkedIdentityField(view_name='add-new-comment')

    class Meta:
        model = Article
        fields = ['title', 'author', 'text', 'pub_date', 'comments', 'add_new_comment']
