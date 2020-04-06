from django.contrib import admin
from .models import Place, Listing, HeatingChoices, Saved, SearchProfiles, Comment, Image


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('region', 'city')
    search_fields = ('region', 'city')
    list_filter = ('region', )


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    # @TODO: Add fieldsets for better overview in the Admin
    # @TODO: Add images inline for each listing

    list_display = ('zip_code', 'cover_image', 'title', 'user', 'city', 'is_approved')
    search_fields = ('city', 'title', 'description', 'user')
    list_filter = ('is_approved', 'zip_code')
    readonly_fields = ('times_visited', 'soft_deleted' )
    actions = ['approve', ]

    def approve(self, request, queryset):
        count = queryset.filter(is_approved=None).update(is_approved=True)
        if count:
            self.message_user(request, f"{count} listings have been approved!")
    approve.short_description = 'Approve listings'


@admin.register(SearchProfiles)
class SearchProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'city', 'price_from', 'price_to', 'frequency')


@admin.register(HeatingChoices)
class HeatingChoicesAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(Saved)
class SavedAdmin(admin.ModelAdmin):
    list_display = ('user', 'listing')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'listing', 'body')


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('listing', 'image', 'order')
    list_filter = ('listing', )
    search_fields = ('listing', )

