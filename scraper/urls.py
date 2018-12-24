from rest_framework.routers import SimpleRouter
from django.conf.urls import url
from scraper import views


router = SimpleRouter()

# router.register(r'artist', views.ArtistViewSet, 'Artist')
router.register(r'user', views.UserViewSet, 'User')

urlpatterns = router.urls + [url(r'^find_me/(?P<artist_name>[^/.]+)/(?P<song_title>[^/.]+)/(?P<fb_id>[^/.]+)/$', views.find_me),
                             url(r'^policy/', views.policy)]
