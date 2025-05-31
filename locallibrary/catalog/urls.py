from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('brews/', views.BrewListView.as_view(), name='brews'),
    path('brew/<int:pk>', views.BrewDetailView.as_view(), name='brew-detail'),
    path('register/', views.register, name='register'),
]