from django.db import models
from django.urls import reverse # Used to generate URLs by reversing the URL patterns
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass


class BrewType(models.Model):
    """Model representing a brew brewType."""
    name = models.CharField(max_length=200, help_text='Enter a brew brewType (e.g. Stout, Green Tea, Espresso)')

    def __str__(self):
        """String for representing the Model object."""
        return self.name

class Brewer(models.Model):
    """Model representing a brewer."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Retired', null=True, blank=True)
    class Meta:
        ordering = ['last_name', 'first_name']
    def get_absolute_url(self):
        return reverse('brewer-detail', args=[str(self.id)])
    def __str__(self):
        return f'{self.last_name}, {self.first_name}'

class Brew(models.Model):
    """Model representing a brew (not a specific tasting)."""
    title = models.CharField(max_length=200)
    brewer = models.ManyToManyField('Brewer', help_text='Enter a brew brewer')
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the brew')
    code = models.CharField('Brew Code', max_length=13, unique=True, help_text='Unique code for the brew')
    brewType = models.ManyToManyField(BrewType, help_text='Select a brewType for this brew')
    def display_brewer(self):
        return ', '.join(brewer.__str__() for brewer in self.brewer.all()[:3])
    display_brewer.short_description = 'Brewer'
    def display_brewType(self):
        return ', '.join(brewType.name for brewType in self.brewType.all()[:3])
    display_brewType.short_description = 'BrewType'
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('brew-detail', args=[str(self.id)])


