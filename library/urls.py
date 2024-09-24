from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="library"),
    path("booksStorage/", views.BooksStorageListView, name="books-storage"),
    path("book/<pk>", views.BookDetailView.as_view(), name="book-detail"),
    path('add-book/', views.addOrEditBookView, name='add-book'),
    path('edit-book/<int:bookId>/', views.addOrEditBookView, name='edit-book'),
]
