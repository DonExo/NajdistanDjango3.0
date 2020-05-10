from django.contrib import admin
from django_celery_beat.models import IntervalSchedule, SolarSchedule, ClockedSchedule


# @admin.register(CommentReport)
class CommentReportAdmin(admin.ModelAdmin):
    list_display = ('comment', 'reason', 'reporter')
    search_fields = ('reporter', )


# @admin.register(ListingReport)
class ListingReportAdmin(admin.ModelAdmin):
    list_display = ('listing', 'reporter', 'reason')
    search_fields = ('listing', 'reporter')


###############################################
### Remove unnecessary Cronjob ModelAdmins ####

admin.site.unregister(IntervalSchedule)
admin.site.unregister(SolarSchedule)
admin.site.unregister(ClockedSchedule)
