from email import message
from django.db import models
from ckeditor.fields import RichTextField
from autoslug import AutoSlugField
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from . utils import Util
# Create your models here.

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=25, null=True)
    slug = AutoSlugField(populate_from="name", unique=True, always_update=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = 'Categories'

class Article(models.Model):
    NEWS_STATUS = (
        ('BREAKING', 'BREAKING'),
        ('TRENDING', 'TRENDING')
    )

    admin = models.ForeignKey(User, related_name="articles", on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=300, null=True)
    text = RichTextField(config_name = "awesome_ckeditor", null=True)
    slug = AutoSlugField(populate_from="title", unique=True, always_update=True)
    category = models.ForeignKey(Category, related_name="articles", on_delete=models.CASCADE)
    featured = models.BooleanField(default=False)
    status = models.CharField(max_length=200, choices=NEWS_STATUS, null=True, blank=True)
    image = models.ImageField(upload_to="news/articles/", null=True)
    views = models.IntegerField(default="0", null=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.title)

    @property
    def get_absolute_url(self):
        return reverse('article-detail', kwargs={'article_slug': self.slug})

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = '' #set default image
        return url

    class Meta:
        ordering = ['-timestamp']

class ArticleViews(models.Model):
    article = models.ForeignKey(Article, related_name="articles", on_delete=models.CASCADE)
    ip = models.CharField(max_length=100, null=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.ip)

class Comment(models.Model):
    article = models.ForeignKey(Article, related_name="comments", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(null=True)
    website = models.URLField(blank=True, null=True)
    message = models.TextField(null=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.name)

    @property
    def nice_timestamp(self):
        return Util.sweet_timestamp(self.timestamp, timezone.now())

class Reply(models.Model):
    comment = models.ForeignKey(Comment, related_name="replies", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(null=True)
    message = models.TextField(null=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.name)

    @property
    def nice_timestamp(self):
        return Util.sweet_timestamp(self.timestamp, timezone.now())

    class Meta:
        verbose_name_plural = 'Replies'