from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from scraper.serializers import ArtistSerializer, SongSerializer
from scraper.models import Artist, Song
from django.http import HttpResponse
import requests
import bs4
import json


def get_infos(url, page=0, indent=0):
    infos_page = requests.get(url + str(page))
    infos_page.raise_for_status()

    infos_object = bs4.BeautifulSoup(infos_page.text, "html.parser")
    next = infos_object.find('a', text='>')
    if next:
        next = next.get('href')

    infos = []

    infos_ugly = infos_object.select('td a')
    infos_ugly_length = int(len(infos_ugly) / 3)

    for i in range(infos_ugly_length):
        if infos_ugly[i].get('class') == "button":
            continue
        info = {}
        info['name'] = infos_ugly[i * 3].getText()
        info['url'] = infos_ugly[(i * 3) + indent].get('href')
        infos.append(info)

    return infos, next


def scrap(request, page):
    page_in_url = page * 20

    artists, next_artists = get_infos('http://tononkira.serasera.org/tononkira/mpihira/results/', page_in_url, 1)

    for artist in artists:
        post_data = {'name': artist['name']}
        response = requests.post('https://mozikascraper.herokuapp.com/scraper/artist/', data=post_data)
        artist_id = json.loads(response.content)['id']
        next_songs = artist['url']
        while next_songs:
            songs, next_songs = get_infos(next_songs, '', 0)
            for song in songs:
                post_daty = {'name': song['name'], 'artist': artist_id, 'lyrics': 'hello'}
                requests.post('https://mozikascraper.herokuapp.com/scraper/song/', data=post_daty)

    html = "<html><body>Next page: %s.</body></html>" % (page_in_url + 20)
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
