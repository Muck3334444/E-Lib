from django.shortcuts import render
from django.views import generic

from library.models import Book
# Create your views here.


def index(request):
    return render(request, "index.html")

def BooksListView(request):
    context = {
        "books": Book.objects.all()
    }
    return render(request, "books_list.html", context=context)

class BookDetailView(generic.DetailView):
    model = Book