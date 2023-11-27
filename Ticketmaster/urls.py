from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="ticketmaster"),
    path('profile_list/', views.profile_list, name="profile_list"),
    path('login/', views.log_in, name="login"),
    path('logout/', views.log_out, name="logout"),

]