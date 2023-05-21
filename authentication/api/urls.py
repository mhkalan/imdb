from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path
from .views import *


urlpatterns = [
    path('login', obtain_auth_token, name='login'),
    path('register', registration_view, name='registration'),
    path('logout', logout_view, name='registration'),

]




