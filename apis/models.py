from django.db import models

# Create your models here.
class Topic(models.Model):
    title = models.CharField(max_length=50)
    category = models.CharField(max_length=10)
    cluster = models.IntegerField(blank=True)
    main = models.TextField()
    author = models.CharField(max_length=10)
    # tag = models.CharField(blank=True)
    youtube_link = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at',)

class Question(models.Model):
    category = models.CharField(max_length=10)
    main = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at',)

class Tag(models.Model):
    tag = models.CharField(max_length=10)

    class Meta:
        ordering = ('created_at')