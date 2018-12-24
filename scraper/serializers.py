from rest_framework.serializers import ModelSerializer
from scraper.models import Artist, Song, User


class ArtistSerializer(ModelSerializer):

    class Meta:
        model = Artist
        fields = '__all__'


class SongSerializer(ModelSerializer):

    class Meta:
        model = Song
        fields = '__all__'

class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
