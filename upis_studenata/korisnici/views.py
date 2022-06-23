from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView, FormView
from korisnici.models import Korisnici
from predmeti.models import Predmeti, Upisi
from .forms import KorisniciForm, KorisniciUpdateForm, SetPasswordForm
from django.urls import reverse_lazy, reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.

class SetPasswordView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, FormView):
  form_class = SetPasswordForm
  template_name = 'korisnici/admin_change_password.html'
  success_message = 'Uspješno promijenjena lozinka.'

  def get_success_url(self):
    return reverse_lazy('korisnici_details', kwargs={'pk': self.kwargs['user_id']})

  def test_func(self):
    return self.request.user.role == 'Admin'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['page_title'] = 'Promjena Lozinke'
    context['korisnik'] = Korisnici.objects.get(id=self.kwargs['user_id'])
    return context

  def get_form_kwargs(self):
      kwargs = super(SetPasswordView, self).get_form_kwargs()
      user = Korisnici.objects.get(id=self.kwargs['user_id'])
      kwargs['user'] = user
      return kwargs

  def form_valid(self, form):
      form.save()
      return super(SetPasswordView, self).form_valid(form)


def error_404_view(request, exception):
    return render(request, '404.html', {'page_title': '404 Not Found'})

def home_view(request):
  return render(request, 'home.html', {'page_title': 'Početna'})

def logout_view(request):
  logout(request)
  return redirect(reverse('user_login'))

def login_view(request):
  if request.method == 'POST':
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    if not username or not password:
      return redirect(reverse('home'))
    user = authenticate(request, username=username, password=password)
    if user:
      login(request, user)
      messages.success(request, f'Uspješno ste prijavljeni kao {username}.')
      return redirect(reverse('home'))
    else:
      messages.error(request, f'Niste unijeli ispravne podatke. Pokušajte ponovno.')
      return redirect(reverse('user_login'))
  elif request.method == 'GET':
    if not request.user.is_authenticated:
      return render(request, 'korisnici/login.html', {'page_title': 'Prijava'})
    else:
      return redirect(reverse('home'))

class KorisniciCreateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
  form_class = KorisniciForm
  template_name = 'korisnici/korisnici_form.html'
  success_url = reverse_lazy('korisnici_create')
  success_message = "%s uspješno dodan!"

  def get_initial(self):
    return {
      'role': self.request.GET.get('role', None)
    }

  def test_func(self):
    return self.request.user.role == 'Admin'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['page_title'] = 'Dodaj Predmet'
    return context

  def get_success_message(self, cleaned_data):
    return self.success_message %(self.object.role)

  def get_success_url(self):
    return reverse_lazy('korisnici_details',args=(self.object.id,))

class KorisniciListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
  model = Korisnici
  template_name = 'korisnici/korisnici_list.html'
  paginate_by = 20
  context_object_name = 'korisnici'

  def test_func(self):
    return self.request.user.role == 'Admin'

  def get_queryset(self):
    role = self.request.GET.get('role', None)
    return self.model.objects.filter(role__name__iexact=role) if role else self.model.objects.all()

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['page_title'] = 'Popis Korisnika'
    role = self.request.GET.get('role', None)
    context['searched_role'] = role if role else '*'
    return context

class KorisniciDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
  model = Korisnici
  context_object_name = 'korisnik'

  def test_func(self):
    return self.request.user.role == 'Admin'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['page_title'] = 'Detalji Korisnika'
    user = self.model.objects.get(id=self.kwargs['pk'])
    if user.role == 'Student':
      context['predmeti_count'] = Upisi.objects.filter(student_id=user).count()
    elif user.role == 'Profesor':
      context['predmeti_count'] = Predmeti.objects.filter(nositelj=user).count()
    return context

class KorisniciUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
  model = Korisnici
  form_class = KorisniciUpdateForm
  template_name = 'korisnici/korisnici_form.html'
  success_message = "Korisnik uspješno izmijenjen!"

  def test_func(self):
    return self.request.user.role == 'Admin'

  def dispatch(self, request, *args, **kwargs):
    print(self.get_object())
    return super().dispatch(request, *args, **kwargs)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['page_title'] = 'Uredi Korisnika'
    return context

  def get_success_url(self):
    return reverse_lazy('korisnici_details', kwargs={'pk': self.object.pk})

class KorisniciDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
  model = Korisnici
  success_message = "Korisnik %s je uspješno izbrisan"
  success_url = reverse_lazy('korisnici_list')
  context_object_name = 'korisnik'

  def test_func(self):
    return self.request.user.role == 'Admin'

  def get_success_message(self, cleaned_data):
    return self.success_message %(self.object)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['page_title'] = 'Izbriši Korisnika'
    return context

@login_required
def upisni_list_view(request, pk):
  if request.user.role == 'Admin' or request.user.id == pk:
    context = {}
    context['page_title'] = 'Upisni List'
    korisnik = Korisnici.objects.get(id=pk)
    if korisnik.role != 'Student':
      return redirect(reverse('korisnici_details', kwargs={'pk': pk}))
    context['korisnik'] = korisnik
    context['upisani_predmeti'] = Upisi.objects.filter(student_id=pk)
    context['predmeti'] = Predmeti.objects.exclude(pk__in=korisnik.upisani_predmeti.all()).order_by('naziv')
    return render(request, 'korisnici/upisni_list.html', context)
  else:
    return redirect(reverse('korisnici_details', kwargs={'pk': pk}))

class ProfesorPredmetListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
  model = Predmeti
  template_name = 'korisnici/predmeti_list_nositelj.html'
  paginae_by = 20
  context_object_name = 'predmeti'

  def test_func(self):
    return self.request.user.role == 'Admin' or self.request.user.id == self.kwargs['pk']

  def get_queryset(self):
    profesor_id = self.kwargs['pk']
    return self.model.objects.filter(nositelj=profesor_id).order_by('naziv')

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['page_title'] = 'Popis Predmeta Profesora'
    context['profesor'] = Korisnici.objects.get(id=self.kwargs['pk'])
    return context
