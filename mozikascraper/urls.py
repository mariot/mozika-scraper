from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
admin.autodiscover()


# Examples:
# url(r'^$', 'mozikascraper.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^scraper/', include('scraper.urls')),
]
