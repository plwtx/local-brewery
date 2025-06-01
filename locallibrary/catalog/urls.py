from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('brews/', views.BrewListView.as_view(), name='brews'),
    path('my-journal/', views.UserBrewListView.as_view(), name='my-journal'),
    path('brew/<uuid:pk>/', views.BrewDetailView.as_view(), name='brew-detail'),
    path('add-brew/', views.BrewCreateView.as_view(), name='add-brew'),
    path('edit-brew/<uuid:pk>/', views.BrewUpdateView.as_view(), name='edit-brew'),
    path('delete-brew/<uuid:pk>/', views.BrewDeleteView.as_view(), name='delete-brew'),
    path('register/', views.register, name='register'),
]