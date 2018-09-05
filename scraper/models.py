from django.db import models

# Create your models here.


class Artist(models.Model):
    name = models.CharField(max_length=100)
    real_name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name


class Song(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    real_title = models.CharField(max_length=100, null=True)
    lyrics = models.TextField()

    def __str__(self):
        return self.title
