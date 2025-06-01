from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import BrewPost, BREW_METHOD_CHOICES
import datetime

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = get_user_model()
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password2'].label = "Confirm pass"
        self.fields['password2'].help_text = "Enter the same password as before, for verification."

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user

class DurationWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = (
            forms.NumberInput(attrs={'placeholder': 'Minutes', 'class': 'duration-input'}),
            forms.NumberInput(attrs={'placeholder': 'Seconds', 'class': 'duration-input'})
        )
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            minutes = value.seconds // 60
            seconds = value.seconds % 60
            return [minutes, seconds]
        return [0, 0]

class DurationField(forms.MultiValueField):
    widget = DurationWidget

    def __init__(self, *args, **kwargs):
        fields = (
            forms.IntegerField(min_value=0),
            forms.IntegerField(min_value=0, max_value=59)
        )
        super().__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            minutes, seconds = data_list
            return datetime.timedelta(minutes=minutes, seconds=seconds)
        return None

class BrewPostForm(forms.ModelForm):
    brew_time = DurationField(help_text='Enter minutes and seconds')

    class Meta:
        model = BrewPost
        fields = ['brew_name', 'brew_type', 'brew_method', 'brew_time', 
                 'seed_origin', 'seed_name', 'roast_level', 'rating', 'notes']
        widgets = {
            'rating': forms.Select(choices=[(i, str(i)) for i in range(1, 11)]),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If instance exists and has a brew_type, filter brew_method choices
        if self.instance and self.instance.brew_type:
            self.fields['brew_method'].choices = BREW_METHOD_CHOICES.get(self.instance.brew_type, [])