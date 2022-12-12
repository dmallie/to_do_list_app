from django.shortcuts import render, redirect, get_object_or_404
from . import forms 
from . import models
# To authenticate the login information
from django.contrib import messages, auth 
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.mixins import LoginRequiredMixin
# activation link packages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator 
# email message packages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string 
from django.core.mail import EmailMessage

# Create your views here.
def sign_up(request):
       if request.method == 'POST':
# create a form object
              form = forms.SignUpForm(request.POST)
# validate the information in the form
                    
              if form.is_valid():
                     first_name = form.cleaned_data['first_name']
                     print("in sign_up")
                     last_name = form.cleaned_data['last_name']
                     email = form.cleaned_data['email']
                     phone_number = form.cleaned_data['phone_number']
                     password = form.cleaned_data['password']
                     gender = request.POST.get('gender')
                     username = email.split('@')[0]
# create a user account
                     user = models.UserAccount.objects.create_user(
                            first_name, last_name, email, phone_number, gender, password
                     )
                     form = forms.SignUpForm()
#Prepare the verificaton email
                     verification_content = {
                            'domain': get_current_site(request),
                            'user': request.user,
                            'token': default_token_generator.make_token(user),
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                     }
# the body part o the email
                     message = render_to_string('accounts/account_verification.html', verification_content)
# subject part of the email
                     subject = "activation link for calendar app"
# the destination email or user email address
                     to_email = email 
# Compose the verification email
                     compose_email = EmailMessage(subject, message, to = [to_email])
# send the verification email 
                     compose_email.send()                     

                     return redirect('/accounts/login/?command=verification&email='+to_email)
       else: 
              form = forms.SignUpForm()
              print("post is not working")
       context = {
              'form_password': form['password'],
              'form_confirm' : form['confirm_password'],
              'form': form,
       }
       return render(request, 'accounts/sign_up.html', context=context)
# Activate the newly created account
def activate(request, uidb64, token):
# decode uid 
       try:
              uid = urlsafe_base64_decode(uidb64).decode()
              user = models.UserAccount._default_manager.get(pk=uid)
       except(TypeError, ValueError, OverflowError, models.UserAccount.DoesNotExist):
              user = None 
# decode  the token 
       if user is not None and default_token_generator.check_token(user, token):
              user.is_active = True 
              user.save()
              messages.success(request, 'Congratulations! Your account is activated.')
              return redirect('accounts:login')
       else:
              messages.error(request, 'Activation link has expired')
              return redirect('accounts:sign_up')

# Create profile page
@login_required(login_url = 'accounts:login')
def create_profile(request):
       if request.method == 'POST':
# create a form object
              form = forms.CreateProfileForm(request.POST)
# create an empty UserProfile object
              userProfile = models.UserProfile()
              if form.is_valid():
                     userProfile.address = form.cleaned_data['address']
                     userProfile.postal_code = form.cleaned_data['postal_code']
                     userProfile.city = form.cleaned_data['city']
                     userProfile.state = form.cleaned_data['state']
                     userProfile.country = form.cleaned_data['country']

                     if len(request.FILES) != 0:
                            userProfile.profile_picture = request.FILES['profile_img']
                     userProfile.user = request.user 
# After we successfully fetched infromation from the page, time to save it on the database
                     userProfile.save()
# After we save the data prompt a success message
                     messages.success(request, "Thanks! You have successfully created your profile page")
# finally return the page to login 
                     return redirect('accounts:my_profile')
              else:
                     messages.error(request, "Please check your infomations")
       else:
              form = forms.CreateProfileForm()
       context = {
              'form': form,
       }

       return render(request, 'accounts/create_profile.html', context)

# Login 
def login(request):
       if request.method == 'POST':
# fetch the email address and password from the page
              email = request.POST.get('email')
              password = request.POST.get('password')
# authenticate the user using Django auth class
              user = auth.authenticate(email=email, password=password)
              if user is not None:
                     auth.login(request, user)
                     messages.success(request, 'You are logged in')
                     url = request.META.get('HTTP_REFERER')
                     return redirect('calendar_app:index')
              else:
                     print("in the else block")
                     messages.error(request, 'Invalid login credentials')
       return render(request, 'accounts/login.html')
# Superuse Signup 
def superuser_signup(request):
       if request.method == 'POST':
# create a form object
              form = forms.SignUpForm(request.POST)
# validate the information in the form             
              if form.is_valid():
                     first_name = form.cleaned_data['first_name']
                     last_name = form.cleaned_data['last_name']
                     email = form.cleaned_data['email']
                     phone_number = form.cleaned_data['phone_number']
                     password = form.cleaned_data['password']
                     gender = request.POST.get('gender')
                     username = email.split('@')[0]
# create a user account
                     user = models.UserAccount.objects.create_superuser(
                            first_name, last_name, email, phone_number, gender, password
                     )
                     form = forms.SignUpForm()
                     print('user: ', user)
       else: 
              form = forms.SignUpForm()
              print("post is not working")
       context = {
              'form_password': form['password'],
              'form_confirm' : form['confirm_password'],
              'form': form,
       }
       return render(request, 'accounts/superuser_signup.html', context=context)
# To display profile page

@login_required(login_url = 'accounts:login')
def my_profile(request):
       try:
# find who the current user is 
              current_user = request.user
# get the current user's profile data
              user_profile = models.UserProfile.objects.get(user = current_user)
              if user_profile is None:
                     return redirect('accounts:create_profile')
       except Exception as e:
              raise e 
       print("user_profile: ", user_profile)
       context = {
              'profile': user_profile,
       }
       return render(request,'accounts/my_profile.html',context)

@login_required(login_url = 'login')
def edit_profile(request):
# display the edit profile page
       try:
# find who the current user is 
              current_user = request.user
# get the current user's profile data
              user_profile = models.UserProfile.objects.get(user = current_user)
       except Exception as e:
              raise e 
# get the fields that needs to be updated
       update_fields = []
       if request.method == 'POST':
              if request.POST.get('update_names') != None:
                     update_fields.append('update_names')
              if request.POST.get('email') == 'on':
                     update_fields.append('email')
              if request.POST.get('phone_number') == 'on':
                     update_fields.append('phone_number')
              if request.POST.get('gender') == 'on':
                     update_fields.append('gender')
              if request.POST.get('address') == 'on':
                     update_fields.append('address')
              if request.POST.get('postal_code') == 'on':
                     update_fields.append('postal_code')
              if request.POST.get('city') == 'on':
                     update_fields.append('city')
              if request.POST.get('state') == 'on':
                     update_fields.append('state')
              if request.POST.get('country') == 'on':
                     update_fields.append('country')
              if request.POST.get('profile_img') == 'on':
                     update_fields.append('profile_img')
              update_fields_dic = {
                     'update_fields': update_fields,
              }
              request.session['update_fields'] = update_fields_dic
              return redirect('accounts:update_profile')


       context = {
              'profile': user_profile,
       }
       return render(request,'accounts/edit_profile.html',context)
 
@login_required(login_url = 'login')
def update_profile(request):
       update_fields = request.session['update_fields']
       print("session data: ", request.session['update_fields'])
       if request.method == 'POST':
# create form objects
              user = request.user  # get user
              user_profile = models.UserProfile.objects.get(user=user) # get user profile object
              # user_account  = models.UserAccount.objects.get(user=user)
# create a dictionary object which contains all the fields
              account_dict = {
                     'update_names': [ request.POST.get('first_name'), request.POST.get('last_name')],
                     'email': request.POST.get('email'),
                     'phone_number': request.POST.get('phone_number'),
                     'gender': request.POST.get('gender'),
              }
              profile_dict = {
                     'address': request.POST.get('address'),
                     'postal_code': request.POST.get('postal_code'),
                     'city': request.POST.get('city'),
                     'state': request.POST.get('state'),
                     'country': request.POST.get('country'),
                     'profile_img': 'profile_img',
              }
# loop through those fields which needs an update
              for update in update_fields['update_fields']:
                     if update in account_dict:
                            if update == 'update_names':
                                   user.first_name = account_dict[update][0]
                                   user.last_name = account_dict[update][1]
                            if update == 'email':
                                   user.email = account_dict[update]
                            if update == 'phone_number':
                                   user.phone_number = account_dict[update]
                            if update == 'gender':
                                   user.gender = account_dict[update]
                            user.save()
                     if update in profile_dict:
                            if update == 'address':
                                   user_profile.address = profile_dict[update]
                            if update == 'postal_code':
                                   user_profile.postal_code = profile_dict[update]
                            if update == 'city':
                                   user_profile.city = profile_dict[update]
                            if update == 'state':
                                   user_profile.state = profile_dict[update]
                            if update == 'country':
                                   user_profile.country = profile_dict[update]
                            if update == 'profile_img':
                                   if len(request.FILES) != 0:
                                          user_profile.profile_picture = request.FILES['profile_img']
                                            
                            user_profile.save()
                            

              messages.success(request, "Your profile has been updated")
              return redirect('accounts:my_profile')
       context = {
              'profile_pic': models.UserProfile.objects.get(user=request.user),
              'update_fields' : update_fields['update_fields'],
       }

       return render(request,'accounts/update_profile.html',context)

# To logout from the current account
@login_required(login_url='accounts:login')
def logout(request):
       auth.logout(request)
       messages.success(request, 'You are logged out')
       return redirect('accounts:login')

# Forgot Password page
def forgot_password(request):
       if request.method == 'POST':
       # get email address 
              email = request.POST.get('email')
       # check if the email exists in our database
              if models.UserAccount.objects.filter(email=email).exists():
       # if exists then get the owner of the email
                     user = models.UserAccount.objects.get(email__exact=email)
       # send password reset link to the email
                     password_verification = {
                            'domain': get_current_site(request),
                            'user': user,
                            'token': default_token_generator.make_token(user),
                            'uid': urlsafe_base64_encode(force_bytes(user.id)),
                     }
                     print('password_verification[uid]: ', password_verification['uid'])
       # prepare the body part of the email
                     email_body = render_to_string('accounts/reset_password_verification.html', password_verification)
       # prepare the subject part of the email
                     subject = 'Password reset link for calendar app'
       # user email address
                     to_email = email 
       # compose the email
                     compose_email = EmailMessage(subject, email_body, to=[to_email])
       # send the email  
                     compose_email.send()
                     return redirect('password_link_sent')  
              else:
                     print("email does not exist")
                     messages.error(request, 'Email address doesnot exist in our database')  
                     return redirect('forgot_password')          

       return render(request, 'accounts/forgot_password.html')
# Notifying the user that the password resetting link has been sent
def password_link_sent(request):

       return render(request, 'accounts/after_forgot_password.html')
# decodes the Reset password link sent to our email
def activate_reset_password(request, uidb64, token):
# decode the uidb64 and get the user 
       try: 
              uid = urlsafe_base64_decode(uidb64).decode() # decodes the uidb64 & extract uid
              print('uid: ', uid)
# from the uid get the user object
              user = models.UserAccount.objects.get(id = uid)
       except (TypeError, ValueError, OverflowError, models.UserAccount.DoesNotExist):
              user = None
# decode the token
       print('user: ', user)
       if user is not None and default_token_generator.check_token(user, token):
              request.session['uid'] = uid
              messages.success(request, 'Please reset your password')
              return redirect('reset_password')
       else:
              messages.error(request, 'The link has been expired, please request a new one')
              return redirect('forgot_password')

# Reset the password
def reset_password(request):
       if request.method == 'POST':
# get password from reset page
              password_1 = request.POST.get('password')
              password_2 = request.POST.get('confirm_password')
# set the new password to the user
              if password_1 == password_2:
# get the user object from session
                     uid  = request.session.get('uid')
# get the user from its id
                     user = models.UserAccount.objects.get(pk = uid)
                     
                     user.set_password(password_1)
                     user.save()
                     messages.success(request,'The new password has been saved')
                     return redirect('login')
              else:
                     messages.error(request, 'Passwords do not match, Please retype again')
                     return redirect('reset_password')
       
       return render(request,'accounts/reset_password.html')