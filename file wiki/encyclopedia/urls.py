from django.urls import path

from . import views

app_name = 'wiki'
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("search",views.search, name='search'),
    path("new", views.new_entry, name='new_entry'),
    path("edit",views.Edit_Page_choice,name="edit_page_choice"),
    path("edit/<str:title>",views.edit_page,name="edit_page"),
    path("save",views.save_edited_page,name="save_edited_page"),
    path("random",views.random_page,name='random')
]
