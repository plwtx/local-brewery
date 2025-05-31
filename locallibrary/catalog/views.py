from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth import login
from django.urls import reverse_lazy
from .forms import RegistrationForm
from .models import Brew, Brewer, BrewInstance, BrewType

def index(request):
    """View function for home page of site."""
    num_brews = Brew.objects.all().count()
    num_instances = BrewInstance.objects.all().count()
    num_instances_available = BrewInstance.objects.filter(status__exact='a').count()
    num_brewers = Brewer.objects.count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    context = {
        'num_brews': num_brews,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
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
            return redirect('index')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

class BrewListView(generic.ListView):
    model = Brew
    def get_context_data(self, **kwargs):
        context = super(BrewListView, self).get_context_data(**kwargs)
        context['some_data'] = 'This is just some data'
        return context

class BrewDetailView(generic.DetailView):
    model = Brew
