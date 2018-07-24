from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils import timezone
from django.db.models.signals import pre_save
from django.utils.text import slugify



# Create your models here.


def file_size(value): # add this to some file where you can import it from
    limit = 5 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 5 MiB.')

mood_choices = (
    ('happy','happy'),
    ('sad','sad'),
    ('angry','angry'),
    ('spiritual','spiritual'),
    ('general','general'),
    )
activity_choices = (
    ('sleeping','sleeping'),
    ('joking','joking'),
    ('coding','coding'),
    ('driving','driving'),
    ('parting','partying'),
    ('general','general'),

)


class Album(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    artist = models.CharField(max_length=250)
    album_title = models.CharField(max_length=255,unique=True)

    logo = models.ImageField(upload_to="album_logos/",validators=[file_size])
    shared = models.BooleanField(default=False)
    timestamp = models.DateField(default=timezone.now)
    slug = models.SlugField(unique=True)
    mood = models.CharField(max_length=100,
                           choices = mood_choices,default='general')
    activity = models.CharField(max_length=100,choices=activity_choices,default='general')
    timestamp = models.DateTimeField(default=timezone.now,editable=False)

    def get_absolute_url(self):
        return reverse('music:detail',kwargs={'slug':self.slug})

    def __str__(self):
        return self.album_title + ' by '+self.artist

    class Meta:
        ordering=['-timestamp']


def create_new_slug(instance,new_slug=None):
    slug = slugify(instance.album_title)
    if new_slug is not None:
        slug = new_slug
    qs = Album.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug= "%s-%s" %(slug,qs.first().id)
        return create_new_slug(instance,new_slug=new_slug)
    return slug


def album_pre_save_ceiver(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = create_new_slug(instance)


pre_save.connect(album_pre_save_ceiver,sender=Album)

genre_choices = (
    ('Reggae','Reggae'),
    ('Dancehall','Dancehall'),
    ('Hip Hop|Rap','Hip Hop|Rap'),
    ('Country','Country'),
    ('Rnb','Rnb'),
    ('Bongo','Bongo'),
    ('Rock and Roll','Rock and Roll'),
    ('General','General'),

)
# table Song definition
class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    song_file = models.FileField(default=None,max_length=1000)
    song_title = models.CharField(max_length=250)
    is_favorite = models.BooleanField(default=False)
    file_type = models.CharField(max_length=20, default='mp3',blank=True,null=True)
    number_of_plays = models.IntegerField(default=0)
    genre = models.CharField(max_length=100,choices = genre_choices,default='general')
    timestamp = models.DateTimeField(default=timezone.now,editable=False)

    # def save(self, *args, **kwargs):
    #     song_title = self.song_title[:30]
    #     song_title = song_title +'...'
    #     self.slug = slugify(song_title)
    #     super(Song, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('music:detail', kwargs={'slug': self.album.slug})

    class Meta:
        ordering=['-timestamp']


class FromExternalSites(models.Model):
    album = models.ForeignKey(Album,on_delete=models.CASCADE)
    link = models.URLField(blank=False,null=False)
    is_favorite = models.BooleanField(default=False)
    song_title = models.CharField(max_length=10000)
    slug = models.SlugField(unique=True)
    genre = models.CharField(max_length=10,choices=genre_choices,default='general')
    timestamp = models.DateTimeField(default=timezone.now,editable=False)

    def get_absolute_url(self):
        return reverse('music:detail', kwargs={'slug': self.album.slug})

    # def save(self, *args, **kwargs):
    #     song_title = self.song_title[:30]
    #     song_title = song_title +'...'
    #     self.slug = slugify(song_title)
    #     super(FromExternalSites, self).save(*args, **kwargs)

    class Meta:
        ordering=['-timestamp']
