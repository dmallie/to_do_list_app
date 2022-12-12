from django.db import models
from accounts.models import  UserAccount
from django.urls import reverse
from ckeditor.fields import RichTextField
# Create your models here.
class Calendar(models.Model):
       day           = models.IntegerField(null=False, default=1)
       month         = models.IntegerField(null=False, default=1)
       year          = models.IntegerField(null=False, default=2022)
       week_day      = models.IntegerField(null=False, default=1)
       slug          = models.SlugField(max_length=25, unique=True, null=True)

       def __str__(self):
              return self.slug 
       def get_url(self):
              return reverse('calendar_app:schedule_list', args=[self.slug])

class Events(models.Model):
       event_created_at            = models.DateField(auto_now_add = True)
       event_scheduled_to_begin    = models.TimeField(auto_now=False)
       event_scheduled_to_end      = models.TimeField(auto_now=False)
       event_description           = RichTextField(blank=True, null=True)
       event_title                 = models.CharField(max_length=50)
       calendar                    = models.ForeignKey(Calendar, on_delete=models.CASCADE)
       user                        = models.ForeignKey(UserAccount, on_delete=models.CASCADE, default=None)
       def __str__(self):
              return self.event_title 