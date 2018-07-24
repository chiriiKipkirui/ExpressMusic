from django.urls import path
import ngoma.views as ngoma_views
from django.contrib.auth.views import login


app_name = 'ngoma'

urlpatterns = [
    path('albums/', ngoma_views.home, name='home'),
    path('details/<str:album_slug>', ngoma_views.details, name='details'),
    path('logout', ngoma_views.logout_view,name='logout'),
    path('login',login,{'template_name': 'accounts/login.html'},name='login'),
    path('register',ngoma_views.registration_view, name='register'),
    path('add_album',ngoma_views.add_albums,name='add_album'),
    path('<str:album_slug>/add_songs/',ngoma_views.add_song,name='add_song'),
    path('<str:album_slug>/add_songs/from_links',ngoma_views.add_from_links,
    name='add_song_from_links'),
    path('<str:album_slug>/delete',ngoma_views.album_delete_view,name="album_delete"),
    path('<str:album_slug>/songs/<int:song_id>/delete',ngoma_views.delete_song,name="delete_song"),
    path('songs/',ngoma_views.view_songs,name='all_songs'),
    path('<str:album_slug>/songs',ngoma_views.video_player,name="video_player"),
    path('play/',ngoma_views.just_play_view,name='just_play'),
    path('play/search',ngoma_views.search_ajax,name='search_ajax'),
    path('<str:album_slug>/search',ngoma_views.search_ajax_video,name='search_ajax'),
    path('recommend',ngoma_views.music_recommender,name='recommend'),
]
