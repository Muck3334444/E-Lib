from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .forms import BookForm
from .models import Book
from django.contrib.auth.decorators import login_required
from library.models import Book


def index(request):
    return render(request, "index.html")


@login_required
def BooksStorageListView(request):
    context = {
        "books": Book.objects.all()
    }
    return render(request, "booksStorage_list.html", context=context)

@login_required
def addOrEditBookView(request, bookId=None):
    if bookId:
        # Editing an existing book
        book = get_object_or_404(Book, id=bookId)
    else:
        # Creating a new book
        book = None

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()  # Save the form (this will either create or update the book)
            return redirect('books-storage')  # Redirect to the book list page after submission
    else:
        form = BookForm(instance=book)  # Prepopulate the form with the book data if editing

    return render(request, 'addEditBook.html', {'form': form, 'bookId': bookId})



class BookDetailView(generic.DetailView):
    model = Book