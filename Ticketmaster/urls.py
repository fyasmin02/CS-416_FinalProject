from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="ticketmaster"),
    path('profile_list/', views.profile_list, name="profile_list"),
    path('login/', views.log_in, name="login"),
    path('logout/', views.log_out, name="logout"),
    path('addEventFavorite/', views.addEventFavorite, name='addEventFavorite'),
    path('favoritesTab/', views.favoritesTab, name='favoritesTab'),
    path('notes/', views.notes, name='notes'),
    path('add_notes/', views.add_notes, name='add_notes'),
    path('updateNote/', views.updateNote, name='updateNote')
    # path('delete_notes/', views.delete_notes, name='delete_notes')
]