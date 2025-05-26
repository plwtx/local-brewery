from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Brewer, Brew, BrewInstance, BrewType

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

# Inline for BrewInstance in Brew admin
class BrewInstanceInline(admin.StackedInline):
    model = BrewInstance
    extra = 2
# Brew Admin
@admin.register(Brew)
class BrewAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_brewer', 'display_brewType')
    inlines = [BrewInstanceInline]


# BrewInstance Admin
@admin.register(BrewInstance)
class BrewInstanceAdmin(admin.ModelAdmin):
    list_display = ('brew', 'status', 'due_back')
    list_filter = ('status', 'due_back')


# # Create user and save to the database
# user = User.objects.create_user('myusername', 'myemail@crazymail.com', 'myuserpassword')

# # Update fields and then save again
# user.first_name = 'John'
# user.last_name = 'Citizen'
# user.save()
