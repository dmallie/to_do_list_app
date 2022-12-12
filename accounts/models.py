from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager 
# Create your models here.
class AccountManager(BaseUserManager):
# To create a normal user account
       def create_user(self, f_name, l_name, email, p_no, sex, passowrd=None):
# if eamil is None then raise value error
              if email is None:
                     raise ValueError('Email isnot provided')
# if it comes sofar then create a model object and assign it to user object
              user = self.model(
                     first_name    = f_name,
                     last_name     = l_name,
                     email         = self.normalize_email(email),
                     username     = email.split('@')[0],
                     phone_number  = p_no,
                     gender        = sex,
              )
# make username out of email field
              # user_name = email.split('@')[0]
# set password using set_password method
              user.set_password(passowrd)
# save the information by committing it to database
              user.save(using = self._db)
              print('user: ', user)
# return the user object
              return user 
# To create a superuse account 
       def create_superuser(self, f_name, l_name, email, p_no, sex, password=None):
# create a user object which is manifested by the return of create_user method
              user = self.create_user(f_name, l_name, email, p_no, sex, password)
# then we will conver the account to superuser by setting the following fields to True
              user.is_admin        = True
              user.is_active       = True 
              user.is_staff        = True 
              user.is_superadmin   = True
# Now save the configured fields in the user object
              user.save(using = self._db) 
              return user



class UserAccount(AbstractBaseUser):
# set the basic fields for this account
       first_name    = models.CharField(max_length=50)
       last_name     = models.CharField(max_length=50)
       username     = models.CharField(max_length=50, unique=True)
       email         = models.EmailField(max_length=50, unique=True)
       phone_number  = models.CharField(max_length=50)
       gender        = models.CharField(max_length=10)
# fields to be filled by django 
       date_joined   = models.DateTimeField(auto_now=True)
       last_login     = models.DateTimeField(auto_now=True)
# fields to creae a superuse and to activate the account
       is_active     = models.BooleanField(default=False)
       is_staff      = models.BooleanField(default=False)
       is_superadmin = models.BooleanField(default=False)
       is_admin      = models.BooleanField(default=False)
# to set the emai to be used as the username
       USERNAME_FIELD = 'email'
# fields required to be filled
       REQUIRED_FIELD = ['first_name', 'last_name']
# createing AccountManager object 
       objects = AccountManager()
# own methods 
       def __str__(self):
              return self.email 

       def has_perm(self, perm, obj = None):
              return self.is_admin 

       def has_module_perms(self, add_label):
              return True 

class UserProfile(models.Model):
       user          = models.OneToOneField(UserAccount, on_delete=models.CASCADE)
       address       = models.CharField(max_length=50)
       profile_picture = models.ImageField(blank = True, upload_to='userprofile/')
       postal_code   = models.IntegerField()
       city          = models.CharField(max_length=50)
       state         = models.CharField(max_length=50)
       country       = models.CharField(max_length=50) 

       def __str__(self):
              return self.user.email 











