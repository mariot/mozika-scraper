from django.shortcuts import render_to_response
from rest_framework import viewsets
from scraper.serializers import ArtistSerializer, SongSerializer, UserSerializer
from scraper.models import Artist, Song, User, Consultation, MissingSong, FailedConsultation
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
        info['name'] = name
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
        post_data = {'name': artist['name']}
        response = requests.post('https://mozikascraper.hianatra.com/scraper/artist/', data=post_data)
        artist_id = json.loads(response.content.decode('utf-8'))['id']
        next_songs = artist['url']
        i = 0
        while next_songs:
            page_interne = i * 20
            songs, next_songs = get_infos(artist['url'][:-1], page_interne, 0)
            i = i + 1

            for song in songs:
                post_daty = {'title': song['name'],
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


def find_me(request, artist_name, song_title, fb_id):
    user, _ = User.objects.get_or_create(fbid=fb_id)
    artists = list(Artist.objects.values_list('name', flat=True))
    if artists:
        probable_artists = process.extract(artist_name, artists, limit=3)
        if probable_artists and probable_artists[0][1] > 70:
            for artist in probable_artists:
                songs = list(Song.objects.filter(artist__name=artist[0]).values_list('title', flat=True))
                if songs:
                    probable_song = process.extractOne(song_title, songs)
                else:
                    break
                if probable_song and probable_song[1] > 70:
                    song = Song.objects.filter(title=probable_song[0], artist__name=artist[0])[0]
                    artist_obj = song.artist
                    artist_obj.hits += 1
                    artist_obj.save()
                    song.hits += 1
                    song.save()
                    consultation = Consultation(user=user, song=song)
                    consultation.save()
                    del(song.__dict__['_state'])
                    del(song.__dict__['id'])
                    del(song.__dict__['artist_id'])
                    song.__dict__['artist'] = artist[0]
                    return JsonResponse(song.__dict__)
    return JsonResponse({})


def missing_song(request, artist_name, song_title, fb_id):
    user, _ = User.objects.get_or_create(fbid=fb_id)
    missing_song = MissingSong(artist=artist_name, title=song_title)
    missing_song.save()
    failed_consultation = FailedConsultation(user=user, song=missing_song)
    failed_consultation.save()
    return JsonResponse({})

def policy(request):
    return render_to_response('privacypolicy.html')


class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer


class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
