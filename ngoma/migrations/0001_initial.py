# Generated by Django 2.0 on 2018-04-23 09:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import ngoma.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist', models.CharField(max_length=250)),
                ('album_title', models.CharField(max_length=255, unique=True)),
                ('genre', models.CharField(max_length=100)),
                ('logo', models.ImageField(upload_to='', validators=[ngoma.models.file_size])),
                ('shared', models.BooleanField(default=False)),
                ('timestamp', models.DateField(default=django.utils.timezone.now)),
                ('slug', models.SlugField(unique=True)),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FromExternalSites',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.URLField()),
                ('is_favorite', models.BooleanField(default=False)),
                ('song_title', models.CharField(max_length=10000)),
                ('slug', models.SlugField(unique=True)),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ngoma.Album')),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('song_file', models.FileField(default=None, upload_to='')),
                ('song_title', models.CharField(blank=True, max_length=250, null=True)),
                ('is_favorite', models.BooleanField(default=False)),
                ('file_type', models.CharField(blank=True, default='mp3', max_length=20, null=True)),
                ('cover', models.ImageField(blank=True, null=True, upload_to='covers/')),
                ('number_of_plays', models.IntegerField(default=0)),
                ('slug', models.SlugField(unique=True)),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ngoma.Album')),
            ],
        ),
    ]
