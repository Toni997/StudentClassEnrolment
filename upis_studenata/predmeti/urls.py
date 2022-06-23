from django.urls import path
from . import views


urlpatterns = [
  path('', views.PredmetiListView.as_view(), name='predmeti_list'),
  path('dodaj/', views.PredmetiCreateView.as_view(), name='predmeti_create'),
  path('<int:pk>/', views.PredmetiDetailView.as_view(), name='predmeti_details'),
  path('<int:pk>/uredi/', views.PredmetiUpdateView.as_view(), name='predmeti_edit'),
  path('<int:pk>/izbrisi/', views.PredmetiDeleteView.as_view(), name='predmeti_delete'),
  path('<int:pk>/lista-studenata/', views.enrolled_students_view, name='enrolled_students'),
  path('<int:student_id>/upis/<int:predmet_id>/', views.enroll_course, name='enroll_course'),
  path('<int:student_id>/upis/<int:predmet_id>/polozen', views.course_polozen, name='course_polozen'),
  path('<int:student_id>/upis/<int:predmet_id>/izgubljen_potpis', views.course_izgubljen_potpis, name='course_izgubljen_potpis'),
  path('<int:student_id>/ispis/<int:predmet_id>/', views.withdraw_course, name='withdraw_course'),
]
