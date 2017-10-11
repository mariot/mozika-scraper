from rest_framework.routers import SimpleRouter
from django.conf.urls import patterns, url
from scraper import views


router = SimpleRouter()

router.register(r'artist', views.ArtistViewSet, 'Artist')
router.register(r'song', views.SongViewSet, 'Song')

urlpatterns = router.urls + patterns('', url(r'^scrap/(?P<page>\d+)/$', 'scraper.views.scrap'))
