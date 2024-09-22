from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="library"),
    path("books/", views.BooksListView, name="books"),
    path("book/<pk>", views.BookDetailView.as_view(), name="book-detail"),
]
