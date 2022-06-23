from ast import Mod
from django.forms import ModelForm
from korisnici.models import Korisnici
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AdminPasswordChangeForm


class SetPasswordForm(AdminPasswordChangeForm):
  password1 = forms.CharField(label='Nova lozinka', widget=forms.PasswordInput)  
  password2 = forms.CharField(label='Potvrdi lozinku', widget=forms.PasswordInput)
  class Meta:
    labels = {
      'password1': 'Korisničko ime',
    }
  def __init__(self, *args, **kwargs):
    super(SetPasswordForm, self).__init__(*args, **kwargs)
    for visible in self.visible_fields():
      visible.field.widget.attrs['class'] = 'form-control'

class KorisniciForm(UserCreationForm):
  password1 = forms.CharField(label='Lozinka', widget=forms.PasswordInput)  
  password2 = forms.CharField(label='Potvrdi lozinku', widget=forms.PasswordInput)  
  class Meta:
    model = Korisnici
    fields = ['username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'role', 'status']

    labels = {
      'username': 'Korisničko ime',
      'email': 'E-Mail adresa',
      'first_name': 'Ime',
      'last_name': 'Prezime',
      'role': 'Uloga',
    }
  def __init__(self, *args, **kwargs):
    super(KorisniciForm, self).__init__(*args, **kwargs)
    for visible in self.visible_fields():
      visible.field.widget.attrs['class'] = 'form-control'

class KorisniciUpdateForm(ModelForm):
  class Meta:
    model = Korisnici
    fields = ['username', 'email', 'first_name', 'last_name', 'role', 'status']

    labels = {
      'username': 'Korisničko ime',
      'email': 'E-Mail adresa',
      'first_name': 'Ime',
      'last_name': 'Prezime',
      'role': 'Uloga',
    }

  def __init__(self, *args, **kwargs):
    super(KorisniciUpdateForm, self).__init__(*args, **kwargs)
    for visible in self.visible_fields():
      visible.field.widget.attrs['class'] = 'form-control'
    