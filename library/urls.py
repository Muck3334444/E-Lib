from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="library"),
    path("booksStorage/", views.BooksStorageListView, name="books-storage"),
    path("book/<pk>", views.bookDetail, name="book-detail"),
    path('reserve/', views.reserveBook, name='reserve_book'),
    path('rate/', views.giveRating, name='rate_book'),
    path('add-book/', views.addOrEditBookView, name='add-book'),
    path('edit-book/<int:bookId>/', views.addOrEditBookView, name='edit-book'),
    path('add-author/', views.addAuthor, name='add-author'),

]
