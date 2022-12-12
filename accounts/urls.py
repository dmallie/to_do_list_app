from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('sign_up/', views.sign_up, name="sign_up"),
    path('superuser_signup/', views.superuser_signup, name="superuser_signup"),
    path('create_profile/', views.create_profile, name="create_profile"),
    path('my_profile/', views.my_profile, name="my_profile"),
    path('update_profile/', views.update_profile, name="update_profile"),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('activate/<uidb64>/<token>', views.activate, name="activate"),
    path('forgot_password/', views.forgot_password, name="forgot_password"),
    path('password_link_sent/', views.password_link_sent, name="password_link_sent"),
    path('reset_password/', views.reset_password, name="reset_password"),
    path('activate_reset_password/<uidb64>/<token>/', views.activate_reset_password, name="activate_reset_password"),
]
