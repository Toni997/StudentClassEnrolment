from email import message
from tabnanny import verbose
from xml.etree.ElementInclude import include
from django.db import models
from korisnici.models import Korisnici
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.

class Predmeti(models.Model):
  class Meta:
    verbose_name = 'Predmet'
    verbose_name_plural = 'Predmeti'

  class Izborni(models.TextChoices):
    DA = 'da', 'Da'
    NE = 'ne', 'Ne'

  naziv = models.CharField(max_length=255)
  kod = models.CharField(max_length=16)
  nositelj = models.ForeignKey(Korisnici, on_delete=models.SET_NULL, null=True, blank=True)
  program = models.TextField()
  bodovi = models.IntegerField(validators=[MinValueValidator(1, message='Predmet ne može nositi manje od jednog boda.'), MaxValueValidator(60, message='Predmet ne može iznositi više od 60 bodova.')])
  sem_redovni = models.IntegerField(validators=[MinValueValidator(1, message='Broj semestra mora biti između 1 i 16.'), MaxValueValidator(60, message='Broj semestra mora biti između 1 i 16.')])
  sem_izvanredni = models.IntegerField(validators=[MinValueValidator(1, message='Broj semestra mora biti između 1 i 16.'), MaxValueValidator(16, message='Broj semestra mora biti između 1 i 16.')])
  izborni = models.CharField(max_length=10, choices=Izborni.choices, default=Izborni.NE)
  studenti = models.ManyToManyField(Korisnici, through='Upisi', related_name='upisani_predmeti', blank=True, through_fields=('predmet_id', 'student_id'))

  def __str__(self):
    return f'{self.naziv} ({self.kod})'

class Upisi(models.Model):
  class Meta:
    verbose_name = 'Upis'
    verbose_name_plural = 'Upisi'
    unique_together = ('student_id', 'predmet_id')

  class Status(models.TextChoices):
    UPISAN = 'upisan', 'Upisan'
    POLOZEN = 'polozen', 'Položen'
    IZGUBLJEN_POTPIS = 'izgubljen_potpis', 'Izgubljen potpis'

  student_id = models.ForeignKey(Korisnici, on_delete=models.CASCADE, related_name='up_st')
  predmet_id = models.ForeignKey(Predmeti, on_delete=models.CASCADE, related_name='up_pr')
  status = models.CharField(max_length=50, choices=Status.choices, default=Status.UPISAN)

  def __str__(self):
      return f'{self.student_id}, {self.predmet_id}'