from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="ticketmaster"),
    path('profile_list/', views.profile_list, name="profile_list"),
    path('login/', views.log_in, name="login"),
    path('logout/', views.log_out, name="logout"),
    # path('like/<str:event_id>/', views.like, name='like'),
    # path('favorites/', views.favorites, name="favorites"),
    path('add_note/', views.add_note, name='add_note'),
    path('notes/', views.notes, name="notes"),
]