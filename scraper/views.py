from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from scraper.serializers import ArtistSerializer, SongSerializer
from scraper.models import Artist, Song
from django.http import HttpResponse
import requests
import bs4
import json


def get_artists(page):
    artists_page = requests.get('http://tononkira.serasera.org/tononkira/mpihira/results/' + str(page))
    artists_page.raise_for_status()

    artists_object = bs4.BeautifulSoup(artists_page.text, "html.parser")

    artists = []

    artists_ugly = artists_object.select('td a')
    artists_ugly_length = len(artists_ugly) / 3

    for i in range(artists_ugly_length):
        artist = {}
        artist['name'] = artists_ugly[i * 3].getText()
        artist['songsURL'] = artists_ugly[(i * 3) + 1].get('href')
        artists.append(artist)

    return artists

def scrap(request, page):
    page_in_url = page * 20

    artists = get_artists(page_in_url)

    for artist in artists:
        post_data = {'name': artist['name']}
        response = requests.post('https://mozikascraper.herokuapp.com/scraper/artist/', data=post_data)
        artist_id = json.loads(response.content)['id']

    html = "<html><body>Page: %s.</body></html>" % page
    return HttpResponse(html)


class ArtistViewSet(ViewSet):

    def list(self, request):
        queryset = Artist.objects.all()
        serializer = ArtistSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ArtistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        queryset = Artist.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = ArtistSerializer(item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            item = Artist.objects.get(pk=pk)
        except Artist.DoesNotExist:
            return Response(status=404)
        serializer = ArtistSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            item = Artist.objects.get(pk=pk)
        except Artist.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class SongViewSet(ViewSet):

    def list(self, request):
        queryset = Song.objects.all()
        serializer = SongSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = SongSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        queryset = Song.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = SongSerializer(item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            item = Song.objects.get(pk=pk)
        except Song.DoesNotExist:
            return Response(status=404)
        serializer = SongSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            item = Song.objects.get(pk=pk)
        except Song.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)
