from rest_framework.routers import SimpleRouter
from django.conf.urls import url
from scraper import views


router = SimpleRouter()

router.register(r'artist', views.ArtistViewSet, 'Artist')
router.register(r'song', views.SongViewSet, 'Song')

urlpatterns = router.urls + [url(r'^scrap/(?P<page>\d+)/$', views.scrap), url(r'^scrap_artist/(?P<id>\d+)/(?P<artist>\d+)/(?P<page>\d+)/$', views.scrap_artist), url(r'^policy/', views.policy)]
