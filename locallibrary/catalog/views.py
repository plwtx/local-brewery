from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth import login, get_user_model
from django.urls import reverse_lazy
from .forms import RegistrationForm, BrewPostForm
from .models import Brew, Brewer, BrewType, BrewPost
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages

User = get_user_model()

def index(request):
    """View function for home page of site."""
    num_brews = Brew.objects.all().count()
    num_brewers = Brewer.objects.count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    context = {
        'num_brews': num_brews,
        'num_brewers': num_brewers,
        'num_visits': num_visits,
    }
    return render(request, 'index.html', context=context)

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

class BrewListView(ListView):
    """View for displaying all brews (Global Brew History)"""
    model = BrewPost
    template_name = 'catalog/brew_list.html'
    context_object_name = 'brews'
    ordering = ['-post_date']
    paginate_by = 10

class UserBrewListView(LoginRequiredMixin, ListView):
    """View for displaying user's personal brew log"""
    model = BrewPost
    template_name = 'catalog/user_brew_list.html'
    context_object_name = 'brews'
    paginate_by = 10

    def get_queryset(self):
        return BrewPost.objects.filter(user=self.request.user).order_by('-post_date')

class BrewDetailView(DetailView):
    """View for displaying details of a specific brew"""
    model = BrewPost
    template_name = 'catalog/brew_detail.html'
    context_object_name = 'brew'

class BrewCreateView(LoginRequiredMixin, CreateView):
    """View for creating a new brew post"""
    model = BrewPost
    form_class = BrewPostForm
    template_name = 'catalog/brew_form.html'
    success_url = reverse_lazy('my-journal')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Your brew has been posted!')
        return super().form_valid(form)

class BrewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """View for updating an existing brew post"""
    model = BrewPost
    form_class = BrewPostForm
    template_name = 'catalog/brew_form.html'
    success_url = reverse_lazy('my-journal')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Your brew has been updated!')
        return super().form_valid(form)

    def test_func(self):
        brew = self.get_object()
        return self.request.user == brew.user

class BrewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """View for deleting a brew post"""
    model = BrewPost
    success_url = reverse_lazy('my-journal')
    template_name = 'catalog/brew_confirm_delete.html'

    def test_func(self):
        brew = self.get_object()
        return self.request.user == brew.user

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Your brew has been deleted!')
        return super().delete(request, *args, **kwargs)

def home(request):
    """View function for home page of site."""
    # Get counts for site statistics
    num_brews = BrewPost.objects.all().count()
    num_brewers = User.objects.filter(brewpost__isnull=False).distinct().count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    
    # Get latest brews for the homepage
    latest_brews = BrewPost.objects.all().order_by('-post_date')[:5]
    
    context = {
        'num_brews': num_brews,
        'num_brewers': num_brewers,
        'num_visits': num_visits,
        'latest_brews': latest_brews,
    }
    
    return render(request, 'catalog/index.html', context=context)
