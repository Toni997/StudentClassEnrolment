from django.contrib import admin
from .models import Korisnici, Roles

# Register your models here.

admin.site.register(Korisnici)
admin.site.register(Roles)