from django import forms
from . import models

class SignUpForm(forms.ModelForm):
# create a password field and assign attributes to this field
       password = forms.CharField(widget=forms.PasswordInput(attrs={
              'class': 'field_class form-control',
              'placeholder': 'Enter your password',
       }))
       confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
              'class': 'field_class form-control',
              'placeholder': 'Confirm your password',
       }))
       # Gender = [ ('male', 'Male'),
       #               ('female', 'Female'),]
       # gender = forms.CharField(label='Gender',
       #                      widget=forms.RadioSelect(choices=Gender,
       #                                    attrs={'class': 'custom-control-input'}))
       class Meta():
              model = models.UserAccount
              fields = ['first_name','last_name', 'email', 'phone_number', 'gender','password']

# To validat the data the following clean method is created 
       def clean(self):
              cleaned_data = super(SignUpForm, self).clean()
              password = cleaned_data.get('password')
              confirm_password = cleaned_data.get('confirm_password')

              if password != confirm_password:
                     raise forms.ValidationError("Password doesn't match")

# with this init function we initialize the SignUpForm and assign class to the fields
       def __init__(self, *args, **kwargs):
              super(SignUpForm, self).__init__(*args, **kwargs)
              
              for field in self.fields:
                     self.fields[field].widget.attrs['class'] = 'field_class form-control'
              self.fields['first_name'].widget.attrs['placeholder'] = 'First Name'

class CreateProfileForm(forms.ModelForm):
       class Meta():
              model = models.UserProfile
              fields = ['address', 'profile_picture', 'postal_code', 'city', 'state', 'country']

# for priliminary validation we create clean method
       def clean(self):
              cleaned_data = super(CreateProfileForm, self).clean()

       def __init__(self, *args, **kwargs):
              super(CreateProfileForm, self).__init__(*args, **kwargs)

              for field in self.fields:
                     self.fields[field].widget.attrs['class'] = 'field_class form-control'
              self.fields['address'].widget.attrs['placeholder'] = 'Street Name'
