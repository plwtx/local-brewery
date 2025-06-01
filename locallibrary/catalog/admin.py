from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Brewer, Brew, BrewType

# Register simple models
admin.site.register(BrewType)

# Register your custom User model with the admin site
admin.site.register(User, UserAdmin)

# Brewer Admin
class BrewerAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fieldsets = (
        ('General Information', {'fields': ('first_name', 'last_name')}),
        ('Dates', {'fields': (('date_of_birth', 'date_of_death'))}),
    )
admin.site.register(Brewer, BrewerAdmin)

# Brew Admin
@admin.register(Brew)
class BrewAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_brewer', 'display_brewType')
