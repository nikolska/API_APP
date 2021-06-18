import datetime
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()

class Article(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def was_published_recently(self):
        return self.pub_date >= (timezone.now() - datetime.timedelta(days=7))


class Comment(models.Model):
	article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	comment_text = models.TextField()
	pub_date = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f'{self.author} comment for {self.article}'

