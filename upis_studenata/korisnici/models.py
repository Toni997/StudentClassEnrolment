from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class Roles(models.Model):
  class Meta:
    verbose_name = 'Role'
    verbose_name_plural = 'Roles'

  name = models.CharField(primary_key=True, max_length=50)

  def __str__(self):
    return self.name

  def __eq__(self, other: str):
    return self.name == other

class Korisnici(AbstractUser):
  class Meta:
    verbose_name = 'Korisnik'
    verbose_name_plural = 'Korisnici'

  class Status(models.TextChoices):
    NONE = 'none', 'None'
    REDOVNI = 'red', 'Redovni'
    IZVANREDNI = 'izv', 'Izvanredni'

  def __str__(self):
    return f'{self.first_name} {self.last_name} ({self.username})'
 
  role = models.ForeignKey(Roles, on_delete=models.SET_NULL, null=True)
  status = models.CharField(max_length=50, choices=Status.choices, default=Status.NONE)
