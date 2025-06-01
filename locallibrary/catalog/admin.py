from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Brewer, Brew, BrewType, Origin, Seed, BrewPost

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

@admin.register(Origin)
class OriginAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Seed)
class SeedAdmin(admin.ModelAdmin):
    list_display = ('name', 'origin')
    list_filter = ('origin',)
    search_fields = ('name', 'origin__name')

@admin.register(BrewPost)
class BrewPostAdmin(admin.ModelAdmin):
    list_display = ('brew_name', 'user', 'brew_type', 'brew_method', 'rating', 'post_date')
    list_filter = ('brew_type', 'brew_method', 'rating', 'seed_origin', 'roast_level')
    search_fields = ('brew_name', 'user__username', 'notes')
    date_hierarchy = 'post_date'
    readonly_fields = ('post_date',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'brew_name', 'brew_type', 'brew_method')
        }),
        ('Details', {
            'fields': ('brew_time', 'seed_origin', 'seed_name', 'roast_level', 'rating')
        }),
        ('Additional Information', {
            'fields': ('notes', 'post_date')
        }),
    )
