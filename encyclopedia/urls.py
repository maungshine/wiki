from django.urls import path

from . import views

# app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.view_entry, name="view_entry"),
    path("search", views.search, name="search"),
    path("new_entry", views.createNewEntry, name="new_entry"),
    path("random", views.randomPage, name="random"),
    path("edit_entry/<str:title>", views.editEntry, name="edit_entry")
]
