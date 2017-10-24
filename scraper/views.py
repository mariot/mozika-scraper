from django.shortcuts import render_to_response
from rest_framework import viewsets
from django_filters import rest_framework as filters
from scraper.serializers import ArtistSerializer, SongSerializer
from scraper.models import Artist, Song
from django.http import HttpResponse
import requests
import bs4
import json
import unicodedata
import logging


logger = logging.getLogger(__name__)

def get_infos(url, page, indent):
    infos_page = requests.get(url + str(page))
    infos_page.raise_for_status()

    infos_object = bs4.BeautifulSoup(infos_page.text, "html.parser")
    next_obj = infos_object.find('a', text='>')
    if next_obj:
        next_obj = next_obj.get('href')

    infos = []

    infos_ugly = infos_object.select('td a')
    infos_ugly_length = int(len(infos_ugly) / 3)
    if infos_ugly_length > 0:
        if infos_ugly[0].get('class') is not None:
            if infos_ugly[0].get('class')[0] == 'button':
                infos_ugly.pop(0)

    for i in range(infos_ugly_length):
        info = {}
        name = unicodedata.normalize('NFD', infos_ugly[i * 3].getText()).encode('ascii', 'ignore')
        info['name'] = ''.join(e for e in name if str(e).isalnum())
        info['url'] = infos_ugly[(i * 3) + indent].get('href')
        info['other_name'] = infos_ugly[(i * 3) + 1].getText()
        infos.append(info)

    return infos, next_obj


def get_song(url):
    song_page = requests.get(url)
    song_page.raise_for_status()

    song_object = bs4.BeautifulSoup(song_page.text, "html.parser")
    try:
        song_object.find('div', {'class': 'sharebox'}).extract()
        song_object.find('div', {'class': 'adminbox'}).extract()
        song_object.find('div', {'class': 'hevitra'}).extract()
        song_object.find('b').extract()
    except AttributeError:
        pass
    try:
        song = song_object.find('div', {'class': 'col l-2-3 s-1-1'}).getText().encode('ascii', 'ignore')
    except AttributeError:
        song = "Mbola tsy tafiditra ny tononkira"

    return song


def scrap(request, page):
    page_in_url = int(page) * 20
    next_page = int(page) + 1

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

    html = "<html><body><a href='http://127.0.0.1:8000/scraper/scrap/"+str(next_page)+"/'>Next</a></body></html>"
    return HttpResponse(html)


def scrap_artist(request, id, artist, page):
    page_in_url = int(page) * 20
    next_page = int(page) + 1

    songs, next_songs = get_infos('http://tononkira.serasera.org/tononkira/hira/index/' + str(id) + '/', page_in_url, 0)

    for song in songs:
        post_daty = {'title': song['name'], 'artist': artist, 'lyrics': get_song(song['url'])}
        print post_daty
        requests.post('https://mozikascraper.herokuapp.com/scraper/song/', data=post_daty)

    html = "<html><body><a href='http://127.0.0.1:8000/scraper/scrap_artist/"+str(id)+"/"+str(next_page)+"/'>Next</a></body></html>"
    return HttpResponse(html)


def policy(request):
    return render_to_response('privacypolicy.html')


class ArtistViewSet(viewsets.ModelViewSet):

    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer


class SongFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    artist__name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Song
        fields = []


class SongViewSet(viewsets.ModelViewSet):

    queryset = Song.objects.all()
    serializer_class = SongSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('title',)
    filter_class = SongFilter
