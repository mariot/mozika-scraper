from django.contrib import admin
from .models import Artist, Song
from .models import User
from .models import Consultation, FailedConsultation, MissingSong

admin.site.register(Artist)
admin.site.register(Song)
admin.site.register(User)
admin.site.register(Consultation)
admin.site.register(FailedConsultation)
admin.site.register(MissingSong)
