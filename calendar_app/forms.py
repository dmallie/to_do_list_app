from . import models 
from django import forms 

class CreateEventForm(forms.ModelForm):
    
       class Meta():
              model = models.Events
              fields = ('event_title', 'event_description',)

       def __init__(self, *args, **kwargs):
              super(CreateEventForm, self).__init__(*args, **kwargs)
              self.fields['event_title'].widget.attrs['class'] = 'input_field'
              self.fields['event_title'].widget.attrs['placeholder'] = 'Title'

              self.fields['event_description'].widget.attrs['class'] = 'input_field'
              self.fields['event_description'].widget.attrs['placeholder'] = 'Write the task here'


       # widgets = {
       #        'event_description': RichTextField(attrs={'class': 'form-control'}),
       # }
