from django.contrib import admin
from .models import Place, Listing, Saved, Comment, Image


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('region', 'city')
    search_fields = ('region', 'city')
    list_filter = ('region', )


class InlineImagelAdmin(admin.TabularInline):
    model = Image


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    # @TODO: Add fieldsets for better overview in the Admin
    list_display = ('slug', 'title', 'user', 'city', 'price', 'is_approved', 'is_available', 'get_images_count', 'created_at')
    search_fields = ('city', 'title', 'description', 'user')
    list_filter = ('is_approved', 'zip_code')
    readonly_fields = ('slug', 'times_visited', 'soft_deleted' )
    actions = ['approve', 'reject', ]
    inlines = [InlineImagelAdmin, ]

    def approve(self, request, queryset):
        count = queryset.filter(is_approved=None).update(is_approved=True)
        if count:
            self.message_user(request, f"{count} listings have been approved!")
    approve.short_description = 'Approve listings'

    def reject(self, request, queryset):
        count = queryset.update(is_approved=False)
        if count:
            self.message_user(request, f"{count} listings have been rejected!")
    reject.short_description = 'Reject listings'


# @admin.register(Saved)
class SavedAdmin(admin.ModelAdmin):
    list_display = ('user', 'listing')


# @admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'listing', 'body')


# @admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('listing', 'image', 'order')
    list_filter = ('listing', )
    search_fields = ('listing', )
