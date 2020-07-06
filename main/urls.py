from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='homeview'),
    path('register', views.register, name='register'),
    path('login', views.loginPage, name='login'),
    path('logout', views.logoutUser, name='logout'),
    path('<single_slug>', views.single_slug, name='single_slug'),
]
