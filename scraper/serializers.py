from rest_framework.serializers import ModelSerializer
from scraper.models import Artist, Song


class ArtistSerializer(ModelSerializer):

    class Meta:
        model = Artist
        fields = '__all__'


class SongSerializer(ModelSerializer):

    class Meta:
        model = Song
        fields = '__all__'
