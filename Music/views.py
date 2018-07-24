from django.shortcuts import redirect,render
from ngoma.models import Song,Album
from django.http import HttpResponse


def home_base(request):
    # if request.user.is_authenticated:
    #     return redirect('ngoma:home')

    albums = Album.objects.filter(shared=True)
    song_set = ''
    if albums:
        for album in albums:
            song_set = Song.objects.filter(album=album.id)
            for song in song_set:
                # path = song.song_file.path.split('.')
                # print(path)
                # if len(path==3):
                #     song_name = path[1]
                #     song_file_type = path[2]
                #     song.song_title = song_name[60:]
                #     song.file_type = file_type
                #     song.save()
                # else:
                song_name = song.song_file.path[:-4]
                song.song_title = song_name[60:]
                song.file_type = song.song_file.path[-4:]
                song.save()

                song_set = Song.objects.filter(album = album.id)

    context = {
        'songs': song_set,
        'albums': albums
    }

    return render(request, 'main/home_base.html', context)


def login_redirect(request):
    return redirect('ngoma:home')
