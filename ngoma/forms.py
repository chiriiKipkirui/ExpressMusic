from django import forms
from django.contrib.auth.models import User
from .models import Album,Song,FromExternalSites
from django.forms import ModelForm


class RegistrationForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password =forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.CharField(widget=forms.EmailInput)

    class Meta:
        model = User
        fields = ['username', 'password','confirm_password','first_name', 'last_name', 'email']

    # def passwords_validate(*args,**kwargs):
    #     password1 = form.cleaned_data.get('password')
    #     password2 = form.cleaned_data.get('confirm_password')
    #     if password1==password2:
    #         return True
    #     else:
    #         raise validationerror



class AddSongForm(ModelForm):
    class Meta:
        model =Song
        fields = ['song_file','is_favorite','genre']

class AddAlbumForm(ModelForm):
    shared = forms.BooleanField(help_text='All songs under this album would be visible to everybody')

    class Meta:
        model = Album
        exclude =['user','timestamp','slug']

class FromExternalForm(ModelForm):
    link = forms.CharField(help_text="Paste in the link from that favorite site")
    class Meta:
        model = FromExternalSites
        exclude = ['album','slug']
