from django.db import models

# Create your models here.


class Artist(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=100, default='')
    songs_id = models.IntegerField(blank=True, null=True)
    number_of_songs = models.IntegerField(blank=True, default=0)
    hits = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return self.name


class Song(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=100, default='')
    lyrics = models.TextField()
    hits = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return self.title + " - " + self.artist.__str__()


class User(models.Model):
    fbid = models.CharField(max_length=100)
    name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.fbid


class MissingSong(models.Model):
    artist = models.CharField(max_length=100)
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title + " - " + self.artist


class Consultation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.__str__() + " / " + self.song.__str__()


class FailedConsultation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(MissingSong, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.__str__()
