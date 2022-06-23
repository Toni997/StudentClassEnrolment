from urllib.parse import urlparse
from django.urls import path, include
from . import views

urlpatterns = [
  path('', views.KorisniciListView.as_view(), name='korisnici_list'),
  path('dodaj/', views.KorisniciCreateView.as_view(), name='korisnici_create'),
  path('<int:pk>/', views.KorisniciDetailView.as_view(), name='korisnici_details'),
  path('<int:pk>/uredi/', views.KorisniciUpdateView.as_view(), name='korisnici_edit'),
  path('<int:pk>/izbrisi/', views.KorisniciDeleteView.as_view(), name='korisnici_delete'),
  path('<int:pk>/upisni-list/', views.upisni_list_view, name='upisni_list'),
  path('<int:pk>/popis-predmeta/', views.ProfesorPredmetListView.as_view(), name='predmeti_list_nositelj'),
  path('prijava/', views.login_view, name='user_login'),
  path('odjava/', views.logout_view, name='user_logout'),
  path('<int:user_id>/admin-change-password/', views.SetPasswordView.as_view(), name='admin_change_password'),
]
