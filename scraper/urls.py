from rest_framework.routers import SimpleRouter
from django.conf.urls import url
from scraper import views


router = SimpleRouter()

urlpatterns = router.urls + [url(r'^find_me/(?P<artist_name>[^/.]+)/(?P<song_title>[^/.]+)/(?P<fb_id>[^/.]+)/$', views.find_me),
                             url(r'^missing_song/(?P<artist_name>[^/.]+)/(?P<song_title>[^/.]+)/(?P<fb_id>[^/.]+)/$', views.missing_song),
                             url(r'^set_user/(?P<name>[^/.]+)/(?P<fb_id>[^/.]+)/$', views.set_user),
                             url(r'^get_user/(?P<fb_id>[^/.]+)/$', views.get_user),
                             url(r'^policy/', views.policy)]
