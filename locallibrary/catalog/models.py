from django.db import models
from django.urls import reverse # Used to generate URLs by reversing the URL patterns
from django.contrib.auth.models import AbstractUser
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class User(AbstractUser):
    pass

class Origin(models.Model):
    """Model representing a bean/leaf origin."""
    name = models.CharField(max_length=100, unique=True, help_text='Enter a country of origin (e.g., Turkey, Colombia)')
    
    def __str__(self):
        return self.name

class Seed(models.Model):
    """Model representing a bean/leaf type."""
    name = models.CharField(max_length=100, help_text='Enter a bean/leaf name (e.g., Yirgacheffe, Sencha)')
    origin = models.ForeignKey(Origin, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.name

BREW_TYPE_CHOICES = [
    ('Coffee', 'Coffee'),
    ('Tea', 'Tea'),
    ('Beer', 'Beer'),
]

BREW_METHOD_CHOICES = {
    'Coffee': [
        ('French Press', 'French Press'),
        ('Espresso', 'Espresso'),
        ('Pour Over', 'Pour Over'),
        ('Drip', 'Drip'),
        ('Cold Brew', 'Cold Brew'),
    ],
    'Tea': [
        ('Steeping', 'Steeping'),
        ('Cold Brew', 'Cold Brew'),
        ('Gongfu', 'Gongfu'),
    ],
    'Beer': [
        ('Draft', 'Draft'),
        ('Bottle', 'Bottle'),
        ('Can', 'Can'),
    ],
}

ROAST_LEVEL_CHOICES = [
    ('Light', 'Light'),
    ('Medium', 'Medium'),
    ('Dark', 'Dark'),
    ('N/A', 'Not Applicable'),
]

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

class BrewPost(models.Model):
    """Model representing a brew post."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    brew_name = models.CharField(max_length=200)
    brew_type = models.CharField(max_length=10, choices=BREW_TYPE_CHOICES)
    brew_method = models.CharField(max_length=20)
    brew_time = models.DurationField(help_text='Duration in minutes and seconds')
    seed_origin = models.ForeignKey(Origin, on_delete=models.SET_NULL, null=True)
    seed_name = models.ForeignKey(Seed, on_delete=models.SET_NULL, null=True)
    roast_level = models.CharField(max_length=10, choices=ROAST_LEVEL_CHOICES, default='N/A')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text='Rate between 1 and 10'
    )
    notes = models.TextField(blank=True)
    post_date = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-post_date']
        
    def get_absolute_url(self):
        return reverse('brew-detail', args=[str(self.id)])
        
    def __str__(self):
        return f'{self.brew_name} by {self.user.username}'
        
    def clean(self):
        from django.core.exceptions import ValidationError
        # Validate that the brew method matches the brew type
        valid_methods = BREW_METHOD_CHOICES.get(self.brew_type, [])
        if self.brew_method not in [method[0] for method in valid_methods]:
            raise ValidationError({
                'brew_method': f'Invalid brew method for {self.brew_type}. Valid methods are: {", ".join([m[0] for m in valid_methods])}'
            })
        # Only allow roast level for coffee
        if self.brew_type != 'Coffee' and self.roast_level != 'N/A':
            raise ValidationError({
                'roast_level': 'Roast level is only applicable for Coffee'
            })


