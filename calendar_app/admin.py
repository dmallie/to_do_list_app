from django.contrib import admin
from . import models 
from django.utils.html import format_html 
# Register your models here.
class CalendarAdmin(admin.ModelAdmin):
       list_display = ['week_day', 'day', 'month', 'year', 'slug'] 
       readonly_fields = ['week_day', 'day', 'month', 'year', 'slug']
       ordering = ('-year',)
# to present fields lined up in a horizontal direction
       filter_horizontal    = ()
       list_filter          = ()
       fieldsets            = ()
class EventsAdmin(admin.ModelAdmin):
       list_display = ['event_scheduled_to_begin', 'event_created_at',  'event_scheduled_to_end', 'event_title', 'event_description','calendar', 'user']
       readonly_fields = ['event_created_at']
       list_display_link = ['event_scheduled_to_begin', 'event_scheduled_to_end', 'event_title', 'event_description', 'calendar', 'user']
       ordering = ('-event_created_at',)

       filter_horizontal    = ()
       list_filter          = ()
       fieldsets            = ()

admin.site.register(models.Calendar, CalendarAdmin)
admin.site.register(models.Events, EventsAdmin)














