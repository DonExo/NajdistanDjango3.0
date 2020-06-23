from django.contrib import admin

from .models import SearchProfiles


@admin.register(SearchProfiles)
class SearchProfileAdmin(admin.ModelAdmin):
    list_display = ('title', 'pk', 'user', 'city', 'min_price', 'max_price', 'frequency', 'is_active')
