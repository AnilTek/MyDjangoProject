from django.contrib import admin
from django.urls import path 
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('cars/',views.cars,name='cars'),
    path('contact/',views.contact,name='contact'),
    path('houses/',views.houses,name='houses'),
    path('',views.login_request,name='login_request'),
    path('signup/',views.signup_request,name='signup_request'),
    path('resetpassword/',views.resetpassword_request,name='resetpassword_request'),
    path('carmodel/',views.carmodel,name='carmodel'),
    path('loanmodel/',views.loanmodel,name='loanmodel'),
    path('logout/',views.logout_request,name='logout'),
    

]
