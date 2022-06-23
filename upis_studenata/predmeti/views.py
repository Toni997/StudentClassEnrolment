from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from korisnici.models import Korisnici
import predmeti
from predmeti.models import Upisi
from .forms import PredmetiForm, Predmeti
from django.urls import reverse_lazy, reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.

@login_required
def enroll_course(request, student_id, predmet_id):
  if request.method == "POST":
    try:
      student = Korisnici.objects.get(id=student_id)
      predmet = Predmeti.objects.get(id=predmet_id)
    except ObjectDoesNotExist:
      return redirect(reverse('home'))
    if student.role != 'Student':
      return redirect(reverse('home'))
    if request.user.role == 'Admin' or request.user.id == student.id:
      Upisi.objects.get_or_create(student_id=student, predmet_id=predmet)
    return redirect(reverse('upisni_list', kwargs={'pk': student.id}))

@login_required
def course_polozen(request, student_id, predmet_id):
  if request.method == 'POST':
    try:
      upis = Upisi.objects.get(student_id__id=student_id, predmet_id__id=predmet_id)
    except ObjectDoesNotExist:
      return redirect(reverse('home'))
    if request.user.role == 'Admin' or request.user.id == upis.predmet_id.nositelj.id:
      upis.status = 'polozen'
      upis.save()
      if request.user.role == 'Admin':
        return redirect(reverse('upisni_list', kwargs={'pk': student_id}))
      else:
        return redirect(reverse('enrolled_students', kwargs={'pk': predmet_id}))

@login_required
def course_izgubljen_potpis(request, student_id, predmet_id):
  if request.method == 'POST':
    try:
      upis = Upisi.objects.get(student_id__id=student_id, predmet_id__id=predmet_id)
    except ObjectDoesNotExist:
      return redirect(reverse('home'))
    if request.user.role == 'Admin' or request.user.id == upis.predmet_id.nositelj.id:
      upis.status = 'izgubljen_potpis'
      upis.save()
      if request.user.role == 'Admin':
        return redirect(reverse('upisni_list', kwargs={'pk': student_id}))
      else:
        return redirect(reverse('enrolled_students', kwargs={'pk': predmet_id}))

@login_required
def withdraw_course(request, student_id, predmet_id):
  if request.method != 'POST':
    return redirect(reverse('home'))
  try:
    upis = Upisi.objects.get(student_id__id=student_id, predmet_id__id=predmet_id)
  except ObjectDoesNotExist:
    return redirect(reverse('home'))
  if upis.status == 'upisan' and (request.user.role == 'Admin' or request.user.id == upis.student_id.id):
      upis.delete()
      messages.success(request, 'Uspješno ispisan predmet.')
  return redirect(reverse('upisni_list', kwargs={'pk': upis.student_id.id})) if upis else redirect(reverse('home'))

class PredmetiCreateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
  form_class = PredmetiForm
  template_name = 'predmeti/predmeti_form.html'
  success_url = reverse_lazy('predmeti_create')
  success_message = "Predmet uspješno dodan!"

  def test_func(self):
    return self.request.user.role == 'Admin'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['page_title'] = 'Dodaj Predmet'
    return context

  def get_success_url(self):
    return reverse_lazy('predmeti_details',args=(self.object.id,))

class PredmetiListView(ListView):
  queryset = Predmeti.objects.all().order_by('naziv')
  paginate_by = 20
  context_object_name = 'predmeti'

  def test_func(self):
    return self.request.user.role == 'Admin'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['page_title'] = 'Popis Predmeta'
    return context

class PredmetiDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
  model = Predmeti
  context_object_name = 'predmet'

  def test_func(self):
    return self.request.user.role == 'Admin'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['page_title'] = 'Detalji Predmeta'
    context['upisani_studenti'] = Upisi.objects.filter(predmet_id=self.kwargs['pk'])
    return context

class PredmetiUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
  model = Predmeti
  form_class = PredmetiForm
  template_name = 'predmeti/predmeti_form.html'
  success_message = "Predmet uspješno izmijenjen!"

  def test_func(self):
    return self.request.user.role == 'Admin'

  def dispatch(self, request, *args, **kwargs):
    print(self.get_object())
    return super().dispatch(request, *args, **kwargs)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['page_title'] = 'Uredi Predmet'
    return context

  def get_success_url(self):
    return reverse_lazy('predmeti_details', kwargs={'pk': self.object.pk})

class PredmetiDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
  model = Predmeti
  success_message = "Predmet %s je uspješno izbrisan"
  success_url = reverse_lazy('predmeti_list')
  context_object_name = 'predmet'

  def test_func(self):
    return self.request.user.role == 'Admin'

  def get_success_message(self, cleaned_data):
    return self.success_message %(self.object)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['page_title'] = 'Izbriši Predmet'
    return context

@login_required
def enrolled_students_view(request, pk):
  filters = request.GET.getlist('status', [])
  predmet = Predmeti.objects.get(id=pk)
  if(request.user.role != 'Admin' and (not predmet.nositelj or predmet.nositelj.id != request.user.id)):
    return redirect(reverse('home'))
  upisani_studenti = Upisi.objects.none()
  for filt in filters:
    to_include = Upisi.objects.filter(predmet_id=pk, status=filt)
    upisani_studenti = upisani_studenti.union(to_include)
  if not filters:
    upisani_studenti = Upisi.objects.filter(predmet_id=pk)
  paginator = Paginator(upisani_studenti, 20)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  return render(request, 'predmeti/upisani_studenti.html', {'upisani_studenti': upisani_studenti, 'predmet': predmet, 'page_obj': page_obj, 'page_title': 'Upisani Studenti', 'oznaceni_filteri': filters})
