from rest_framework.routers import SimpleRouter
from scraper import views


router = SimpleRouter()

router.register(r'artist', views.ArtistViewSet, 'Artist')
router.register(r'song', views.SongViewSet, 'Song')

urlpatterns = router.urls