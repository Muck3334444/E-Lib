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
    path('book_instance/<pk>', views.getBookInstances, name='book_instances'),
    path('add-author/', views.addAuthor, name='add-author'),
    path('employee/', views.employeeIndex, name='employee-index'),
    path('add_book_instance/', views.addBookInstances, name='add_book_instances')
]
