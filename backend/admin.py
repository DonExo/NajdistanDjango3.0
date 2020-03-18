from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import User, Place, Listing, HeatingChoices


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('region', 'city')
    search_fields = ('region', 'city')
    list_filter = ('region', 'city')


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('zip_code', 'title', 'user', 'city')
    search_fields = ('city', 'title', 'description', 'user')
    list_filter = ('city', 'zip_code')
    readonly_fields = ('times_visited', )


@admin.register(HeatingChoices)
class HeatingChoicesAdmin(admin.ModelAdmin):
    list_display = ('name', )
