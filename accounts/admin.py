from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 
from . import models 
from django.utils.html import format_html 

# Register your models here.
class UserAccountAdmin(UserAdmin):
       list_display = ['first_name', 'last_name', 'username', 'email','gender', 'last_login','date_joined']
       list_display_link = ['first_name', 'last_name', 'username','email']
       readonly_fields = ['last_login', 'date_joined', 'gender']
       ordering = ('-last_login', )
# to present fields lined up in a horizontal direction
       filter_horizontal    = ()
       list_filter          = ()
       fieldsets            = ()

class UserProfileAdmin(admin.ModelAdmin):
       def thumbnail(self, object):
              return format_html('<img src="{}" width="30" style="border-radius:50%;">'.format(object.profile_picture.url))
       thumbnail.short_description = 'Profile Picture'
       list_display = ['thumbnail', 'user', 'city', 'state', 'country']
       list_display_link = ['city', 'state', 'country']
       readonly_fields = ['user', 'thumbnail']
       ordering = ('-country', )

admin.site.register(models.UserAccount, UserAccountAdmin)
admin.site.register(models.UserProfile, UserProfileAdmin)
