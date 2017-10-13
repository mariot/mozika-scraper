from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from scraper.serializers import ArtistSerializer, SongSerializer
from scraper.models import Artist, Song
from django.http import HttpResponse
import requests
import bs4
import json
import logging


def get_infos(url, page, indent):
    infos_page = requests.get(url + str(page))
    infos_page.raise_for_status()

    infos_object = bs4.BeautifulSoup(infos_page.text, "html.parser")
    next = infos_object.find('a', text='>')
    if next:
        next = next.get('href')

    infos = []

    infos_ugly = infos_object.select('td a')
    infos_ugly_length = int(len(infos_ugly) / 3)
    if infos_ugly_length > 0:
        if infos_ugly[0].get('class') != None:
            if infos_ugly[0].get('class')[0] == 'button':
                infos_ugly.pop(0)

    for i in range(infos_ugly_length):
        info = {}
        info['name'] = infos_ugly[i * 3].getText().encode('ascii', 'ignore').strip()
        info['url'] = infos_ugly[(i * 3) + indent].get('href')
        infos.append(info)

    return infos, next


def get_song(url):
    song_page = requests.get(url)
    song_page.raise_for_status()

    song_object = bs4.BeautifulSoup(song_page.text, "html.parser")
    try:
        song_object.find('div', {'class': 'sharebox'}).extract()
        song_object.find('div', {'class': 'adminbox'}).extract()
        song_object.find('div', {'class': 'hevitra'}).extract()
        song_object.find('b').extract()

    return song_object.find('div', {'class': 'col l-2-3 s-1-1'}).getText().encode('ascii', 'ignore').strip()


def scrap(request, page):
    page_in_url = int(page) * 20

    artists, next_artists = get_infos('http://tononkira.serasera.org/tononkira/mpihira/results/', page_in_url, 1)

    for artist in artists:
        post_data = {'name': artist['name']}
        response = requests.post('https://mozikascraper.herokuapp.com/scraper/artist/', data=post_data)
        artist_id = json.loads(response.content)['id']
        next_songs = artist['url']
        i = 0
        while next_songs:
            page_interne = i * 20
            songs, next_songs = get_infos(artist['url'][:-1], page_interne, 0)
            i = i + 1

            for song in songs:
                post_daty = {'title': song['name'], 'artist': artist_id, 'lyrics': get_song(song['url'])}
                requests.post('https://mozikascraper.herokuapp.com/scraper/song/', data=post_daty)

    html = "<html><body>Done!</body></html>"
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
