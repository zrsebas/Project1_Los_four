from django.db import models

# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    image = models.ImageField(upload_to='movie/images/', blank=True, null=True)
    url = models.URLField(blank=True)
    genre = models.CharField(max_length=50, blank=True)
    year = models.IntegerField(null=True, blank=True)


class News(models.Model):
    title = models.CharField(max_length=150)
    desc = models.TextField(blank=True)
    image = models.ImageField(upload_to='news/images/', blank=True, null=True)
    url = models.URLField(blank=True)
    published = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-published']

    def __str__(self):
        return self.title