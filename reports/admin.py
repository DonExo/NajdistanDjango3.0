from django.contrib import admin

from .models import CommentReport, ListingReport


@admin.register(CommentReport)
class CommentReportAdmin(admin.ModelAdmin):
    list_display = ('comment', 'reason', 'reporter')
    search_fields = ('reporter', )


@admin.register(ListingReport)
class ListingReportAdmin(admin.ModelAdmin):
    list_display = ('listing', 'reporter', 'reason')
    search_fields = ('listing', 'reporter')
