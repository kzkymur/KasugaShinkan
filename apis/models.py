from django.db import models

# Create your models here.
class Topic(models.Model):
    serial_num = models.IntegerField(blank=True)
    title = models.CharField(max_length=50)
    category = models.CharField(max_length=10)
    main = models.TextField()
    author = models.CharField(max_length=10)
    youtube_link = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at',)