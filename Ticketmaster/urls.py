from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="ticketmaster"),
    path('profile_list/', views.profile_list, name="profile_list"),
    path('login/', views.log_in, name="login"),
    path('logout/', views.log_out, name="logout"),
    path('addEventFavorite/', views.addEventFavorite, name='addEventFavorite'),
    path('favoritesTab/', views.favoritesTab, name='favoritesTab'),
    # Step 2
    path('', views.view_notes, name="view_notes"),    #Url vor viewing note
    path('add_notes/', views.add_notes, name="add_notes"),  #Url for adding note
    path('update/<int:id>', views.update_note, name="update_note"), #url for updating note
    path('delete/<int:id>', views.delete_note, name="delete_note"), #url for deleting note
]