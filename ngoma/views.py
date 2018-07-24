import os
from itertools import chain
import requests
from django.db.models import Q
from django.shortcuts import render,get_object_or_404,redirect,render_to_response
from django.urls import reverse
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth import logout,authenticate,login
from .models import Song,Album,FromExternalSites
from .forms import RegistrationForm,AddAlbumForm,AddSongForm,FromExternalForm



# Create your views here.
def check_connection():
    url = 'https://www.google.com'
    try:

        resp = requests.get(url)
        if resp.status_code ==200:
            return True
        else:
            return False
    except Exception as e:
        print(e)



def home(request):
    if not request.user.is_authenticated:
        return redirect('/')
    albums = Album.objects.filter(user=request.user.id)
    return render(request, 'main/index.html',{'albums':albums})


def just_play_view(request):
    songs = Song.objects.all()
    connection = check_connection()
    if connection:
        external_songs = FromExternalSites.objects.all()
    else:
        external_songs =[]
    context = {
    'songs':songs,
    'externalsongs':external_songs,
    }
    return render(request,'main/video.html',context)


def details(request, album_slug):
    song_location = settings.MEDIA_URL
    if request.user.is_authenticated:
        album = get_object_or_404(Album, slug=album_slug,user = request.user)
        songs = Song.objects.filter(album=album)
        if check_connection():
            external_songs = FromExternalSites.objects.filter(album=album)
        return redirect('ngoma:video_player',album.slug)
    else:
        album = get_object_or_404(Album,slug=album_slug ,shared = True)
        songs = Song.objects.filter(album =album)
        if check_connection():
            external_songs = FromExternalSites.objects.filter(album=album)
        else:
            external_songs =[]
        return redirect('ngoma:video_player',album.slug)


def logout_view(request):
    logout(request)
    return redirect('home_base')


def registration_view(request):
    form = RegistrationForm(None)
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ngoma:login')
        return render(request, 'accounts/signup.html', {'form': form})
    return render(request, 'accounts/signup.html', {'form':form})


def add_albums(request):
    form =AddAlbumForm(None)
    if request.method =='POST':
        form = AddAlbumForm(request.POST,request.FILES)
        if form.is_valid():
            user = request.user
            artist = form.cleaned_data.get('artist')
            album_title = form.cleaned_data.get('album_title')
            mood =form.cleaned_data.get('mood')
            activity = form.cleaned_data.get('activity')
            logo = form.cleaned_data.get('logo')
            shared = form.cleaned_data.get('shared')
            query = Album.objects.create(user=user,artist=artist,album_title=album_title,
                                         mood=mood,activity=activity,logo=logo,shared=shared)
            query.save()
            return redirect('ngoma:home')
        return render(request,'main/add_album.html',{'form':form})
    return render(request,'main/add_album.html',{'form':form})


def add_song(request,album_slug):
    form = AddSongForm()
    if request.method == 'POST':
        form = AddSongForm(request.POST,request.FILES)
        if form.is_valid():
            album = Album.objects.get(slug=album_slug)
            song_file = form.cleaned_data.get('song_file')
            is_favorite = form.cleaned_data.get('is_favorite')
            genre = form.cleaned_data.get('genre')
            query = Song.objects.create(album=album,
            genre=genre,song_file=song_file,
            is_favorite=is_favorite)
            query.save()
            qs = Song.objects.get(id=query.id)
            song_title = qs.song_file.url[7:-4]
            file_type = qs.song_file.url[-4:]
            qs.song_title = song_title.replace('_',' ').replace('- YouTube','')
            qs.save()
            return redirect('ngoma:details',album.slug)
        return render(request,'main/add_songs.html',{'form':form})
    return render(request,'main/add_songs.html',{'form':form})


def album_delete_view(request,album_slug):
    instance = Album.objects.get(slug=album_slug,user = request.user)
    songs = Song.objects.filter(album=instance)
    for song in songs:
        os.remove(song.song_file.path)
    instance.delete()
    os.remove(instance.logo.path)
    # print(instance.logo.path)
    return redirect('ngoma:home')

def add_from_links(request,album_slug):
    form = FromExternalForm()
    if request.method == 'POST':
        form = FromExternalForm(request.POST)
        if form.is_valid():
            album = Album.objects.get(slug=album_slug)
            song_title = form.cleaned_data.get('song_title')
            is_favorite = form.cleaned_data.get('is_favorite')
            link = form.cleaned_data.get('link')
            genre = form.cleaned_data.get('genre')
            query = FromExternalSites.objects.create(album=album,song_title=song_title,
            link=link, is_favorite=is_favorite,genre=genre)
            query.save()
            return redirect('ngoma:details',album.slug)
        return render(request,'main/add_from_links.html',{'form':form})
    return render(request,'main/add_from_links.html',{'form':form})

def delete_song(request,album_slug,song_id):
    album = Album.objects.filter(slug=album_slug)
    instance = Song.objects.get(pk=song_id)
    instance.delete()
    os.remove(instance.song_file.path)
    return redirect('ngoma:details',album_slug=album_slug)

def view_songs(request):
    songs = Song.objects.all()
    # print(len(songs))

    return render(request,'main/songs.html',{'songs':songs})

def video_player(request, album_slug):
    # song_location = settings.MEDIA_URL
    if request.user.is_authenticated:
        album = get_object_or_404(Album, slug=album_slug,user = request.user)
        songs = Song.objects.filter(album=album)
        if check_connection():
            external_songs = FromExternalSites.objects.filter(album=album)
        else:
            external_songs =[]
        # for song in songs:
        #
        #     song_name = song.song_file.path[:-4]
        #     song.song_title = song_name[60:]
        #     song.file_type = song.song_file.path[-4:]
        #     song.save()

        return render(request, 'main/video.html', {'album': album,
                                                     'songs': songs,
                                                     'external_songs':external_songs})


def search_ajax(request):
    if request.method=='POST':
        search_text = request.POST['search_text']
    else:
        search_text = ''
    Songs = Song.objects.all().filter(song_title__icontains=search_text)
    if check_connection():
        external_songs = FromExternalSites.objects.all().filter(song_title__icontains=search_text)
    else:
        external_songs =[]

    context = {
    'songs':Songs,
    'external_songs':external_songs,
    }

    return render_to_response('main/search_ajax.html',context)


def search_ajax_video(request,album_slug):
    if request.method=='POST':
        search_text = request.POST['search_text']
    else:
        search_text = ''
        album_slug = ''
    album_object = Album.objects.get(slug=album_slug)
    if check_connection():
        external_songs = FromExternalSites.objects.filter(album=album_object.id).filter(
        song_title__icontains=search_text)
    else:
        external_songs =[]


    Songs = Song.objects.filter(album=album_object.id).filter(song_title__icontains=search_text)

    context = {
    'songs':Songs,
    'external_songs':external_songs,
    }

    return render_to_response('main/search_ajax.html',{'songs':Songs})



def music_recommender(request):
    if request.method=='POST':
        mood = request.POST['mood']
        genre = request.POST['genre']
        activity = request.POST['activity']
        if mood!='general':
            mood = mood
            albums_mood = Album.objects.filter(user=request.user).filter(mood=mood)
        else:
            albums_mood = Album.objects.filter(user=request.user).filter(mood=mood)
        if activity!='general':
            activity = activity
            albums_activity = Album.objects.filter(user=request.user).filter(activity=activity)
        else:
            albums_activity = Album.objects.filter(user=request.user).filter(activity=activity)

        if albums_mood:
            if len(albums_mood)>1:
                songs_reccom = [Song.objects.filter(album=alb).filter(genre=genre) for alb in albums_mood]


            else:
                songs_reccom =  Song.objects.filter(album=albums_mood).filter(genre=genre)

        if albums_activity:
            if len(albums_activity)>1:
                songs_reccom = [Song.objects.filter(album=alb).filter(genre=genre) for alb in albums_activity]


            else:
                songs =  Song.objects.filter(album=albums_activity).filter(genre=genre)
        else:
            albums_all = Album.objects.filter(user=request.user)
            songs_reccom = [Song.objects.filter(album=alb).filter(genre=genre) for alb in albums_all]
        songs = []
        for song in songs_reccom:
            for i in song:
                songs.append(i)



    else:
        pass

    return render(request,'main/video.html',{'songs':songs})
