from django.forms import ModelForm
from .models import Predmeti, Korisnici
from django import forms


class PredmetiForm(ModelForm):
  class Meta:
    model = Predmeti
    fields = '__all__'
    labels = {
        'bodovi': 'ECTS bodovi',
        'sem_redovni': 'Semestar (redovni)',
        'sem_izvanredni': 'Semestar(izvanredni)',
    }
    widgets = {
      'bodovi': forms.NumberInput(attrs={'max': 60, 'min': 1}),
      'sem_redovni': forms.NumberInput(attrs={'max': 16, 'min': 1}),
      'sem_izvanredni': forms.NumberInput(attrs={'max': 16, 'min': 1}),
    }

  def __init__(self, *args, **kwargs):
    super(PredmetiForm, self).__init__(*args, **kwargs)
    for visible in self.visible_fields():
      visible.field.widget.attrs['class'] = 'form-control'
    self.fields['nositelj'].queryset = Korisnici.objects.filter(role='Profesor')
    self.fields['studenti'].queryset = Korisnici.objects.filter(role='Student')

