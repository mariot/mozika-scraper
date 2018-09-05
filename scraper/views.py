from django.shortcuts import render_to_response
from rest_framework import viewsets
from django_filters import rest_framework as filters
from scraper.serializers import ArtistSerializer, SongSerializer
from scraper.models import Artist, Song
from django.http import HttpResponse, JsonResponse
from fuzzywuzzy import process
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
        name = unicodedata.normalize('NFD', infos_ugly[i * 3].getText())
        info['name'] = ''.join(e for e in name if str(e).isalnum())
        info['real_name'] = name
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
        song = song_object.find('div', {'class': 'col l-2-3 s-1-1'}).getText()
    except AttributeError:
        song = "Mbola tsy tafiditra ny tononkira"

    return song


def scrap(request, page):
    page_in_url = int(page) * 20
    next_page = int(page) + 1

    artists, next_artists = get_infos('http://tononkira.serasera.org/tononkira/mpihira/results/', page_in_url, 1)

    for artist in artists:
        post_data = {'name': artist['name'], 'real_name': artist['real_name']}
        response = requests.post('https://mozikascraper.hianatra.com/scraper/artist/', data=post_data)
        artist_id = json.loads(response.content.decode('utf-8'))['id']
        next_songs = artist['url']
        i = 0
        while next_songs:
            page_interne = i * 20
            songs, next_songs = get_infos(artist['url'][:-1], page_interne, 0)
            i = i + 1

            for song in songs:
                post_daty = {'title': song['name'], 'real_title': song['real_name'],
                             'artist': artist_id, 'lyrics': get_song(song['url'])}
                requests.post('https://mozikascraper.hianatra.com/scraper/song/', data=post_daty)

    html = "<html><body><a href='https://mozikascraper.hianatra.com/scraper/scrap/"+str(next_page) + \
           "/'>Next</a></body></html>"
    return HttpResponse(html)


def scrap_artist(request, id, artist, page):
    page_in_url = int(page) * 20
    next_page = int(page) + 1

    songs, next_songs = get_infos('http://tononkira.serasera.org/tononkira/hira/index/' + str(id) + '/', page_in_url, 0)

    for song in songs:
        post_daty = {'title': song['name'], 'artist': artist, 'lyrics': get_song(song['url'])}
        requests.post('https://mozikascraper.hianatra.com/scraper/song/', data=post_daty)

    html = "<html><body><a href='https://mozikascraper.hianatra.com/scraper/scrap_artist/" + \
           str(id)+"/"+str(next_page) + "/'>Next</a></body></html>"
    return HttpResponse(html)


def scrap_titles(request, page):
    page_in_url = int(page) * 20
    next_page = int(page) + 1

    artists, next_artists = get_infos('http://tononkira.serasera.org/tononkira/mpihira/results/', page_in_url, 1)

    for artist in artists:
        old_artist = Artist.objects.filter(name=artist['name'])[0]
        old_artist.real_name = artist['real_name']
        old_artist.save()
        next_songs = artist['url']
        i = 0
        while next_songs:
            page_interne = i * 20
            songs, next_songs = get_infos(artist['url'][:-1], page_interne, 0)
            i = i + 1

            for song in songs:
                old_song = Song.objects.filter(title=song['name'])[0]
                old_song.real_title = song['real_name']
                old_song.save()

    html = "<html><body><a href='https://mozikascraper.hianatra.com/scraper/scrap_titles/"+str(next_page) + \
           "/'>Next</a></body></html>"
    return HttpResponse(html)


def find_me(request, artist_name, song_title):
    name = unicodedata.normalize('NFD', artist_name)
    name = ''.join(e for e in name if str(e).isalnum())
    title = unicodedata.normalize('NFD', song_title)
    title = ''.join(e for e in title if str(e).isalnum())
    artists = list(Artist.objects.values_list('real_name', flat=True))
    if artists:
        probable_artists = process.extract(artist_name, artists, limit=3)
        if probable_artists and probable_artists[0][1] > 70:
            for artist in probable_artists:
                songs = list(Song.objects.filter(artist__real_name=artist[0]).values_list('real_title', flat=True))
                if songs:
                    probable_song = process.extractOne(song_title, songs)
                else:
                    break
                if probable_song and probable_song[1] > 70:
                    song = Song.objects.filter(real_title=probable_song[0], artist__real_name=artist[0])[0]
                    del(song.__dict__['_state'])
                    del(song.__dict__['id'])
                    del(song.__dict__['artist_id'])
                    song.__dict__['artist'] = artist[0]
                    return JsonResponse(song.__dict__)
            # old_artist = Artist.objects.get(real_name=probable_artists[0][0])
            # new_song = Song(artist=old_artist, title=title, real_title=song_title, lyrics='Mbola tsy misy')
            # new_song.save()
            return JsonResponse({})
        else:
            # new_artist = Artist(name=name, real_name=artist_name)
            # new_artist.save()
            # new_song = Song(artist=new_artist, title=title, real_title=song_title, lyrics='Mbola tsy misy')
            # new_song.save()
            return JsonResponse({})
    return JsonResponse({})


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
