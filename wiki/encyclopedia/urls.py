from django.urls import path

from . import views

urlpatterns = [    
    path("wiki/", views.index, name="index"),
    path("wiki/<str:title>/", views.entry, name="entry"), #this is by using the hello app url when typing a name will display the desired title
    path("search/", views.search, name="search"),
    path("new/", views.new_page, name="new_page"),
    path("edit_page/", views.edit_page, name="edit_page"),
    path("save_edit/", views.save_edit, name="save_edit"),
    path("random/", views.rand_choice, name="random"),
] 
