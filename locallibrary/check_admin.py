from django.contrib import admin
from django.apps import apps

# Get your models
app_models = apps.get_app_config('catalog').get_models()
print("Models in 'catalog' app:")
for model in app_models:
    print(f"- {model.__name__}")

# Check admin registrations
print("\nAdmin site registrations:")
for model, model_admin in admin.site._registry.items():
    print(f"- {model.__name__} is registered with {model_admin.__class__.__name__}")

# Check auth model setting
from django.conf import settings
print(f"\nAUTH_USER_MODEL = {settings.AUTH_USER_MODEL}")

# Try to get User model
from django.contrib.auth import get_user_model
User = get_user_model()
print(f"get_user_model() returns: {User.__name__} from {User.__module__}")