from django.contrib import admin
from .models import Album, Song,FromExternalSites


# Register your models here.
class AlbumAdmin(admin.ModelAdmin):
    list_display = ['album_title', 'artist', 'user']
    list_display_links = ['album_title']
    search_fields = ['album_title', 'artist']
    list_filter = ['artist', 'timestamp']
    readonly_fields = ['slug','timestamp']


admin.site.register(Album, AlbumAdmin)


class SongAdmin(admin.ModelAdmin):

    list_display = ['song_title', 'album']
    list_filter = ['song_title', 'album', 'genre','is_favorite']
    search_fields = ['song_title', 'is_favorite']
    readonly_fields = ['number_of_plays','file_type']

    class Meta:
        model = Song


admin.site.register(Song, SongAdmin)

class ExternalSitesAdmin(admin.ModelAdmin):
    list_display = ['album','link']
    search_fields = ['album','song_title','genre']
    class Meta:
        model = FromExternalSites

admin.site.register(FromExternalSites,ExternalSitesAdmin)
