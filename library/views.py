from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic

from library.functions import is_employee
from .forms import AuthorForm, BookForm
from .models import Author, Book, BookInstance, Genre, Language, Rating, Reservation
from django.contrib.auth.decorators import login_required, user_passes_test
from library.models import Book
from django.http import JsonResponse
from django.views.decorators.http import require_POST

def index(request):
    return render(request, "index.html")


@login_required
@user_passes_test(is_employee)
def BooksStorageListView(request):
    context = {
        "books": Book.objects.all()
    }
    return render(request, "booksStorage_list.html", context=context)

@login_required
@user_passes_test(is_employee)
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
            book = form.save()  # Save the form (this will either create or update the book)
            selectedLanguages = request.POST.getlist('languages')
            selectedGenres = request.POST.getlist('genres')
            selectedAuthors = request.POST.getlist('authors')
            
            # Set many-to-many relationships
            book.language.set(selectedLanguages)
            book.genre.set(selectedGenres)
            book.author.set(selectedAuthors)
            
            # Save again to finalize M2M relationships
            book.save()

            return redirect('books-storage')  # Redirect to the book list page after submission
    else:
        form = BookForm(instance=book)  # Prepopulate the form with the book data if editing
    
    context = {
        "form": form,
        "bookId": bookId,
        "languages": list(Language.objects.all()),
        "genres": list(Genre.objects.all()),
        "authors": list(Author.objects.all()),
    }

    if book:
        context["selectedLanguages"] = [lang.pk for lang in book.language.all()]
        context["selectedGenres"] = [lang.pk for lang in book.genre.all()]
        context["selectedAuthors"] = [lang.pk for lang in book.author.all()]

    return render(request, 'addEditBook.html', context=context)

@login_required
@user_passes_test(is_employee)
def addAuthor(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('books-storage')
    else:
        form = AuthorForm()
    return render(request, 'addAuthor.html', {'form': form})


def bookDetail(request, pk):
    book = Book.objects.get(pk=pk)

    # Check if the user is authenticated and has an active reservation for this book
    userHasReservation = False
    if request.user.is_authenticated:
        userHasReservation = Reservation.objects.filter(
            bookInstance__book=book, 
            user=request.user, 
            isActive=True
        ).exists()

    # Check if there is a book instance that is not reserved # Todo Add check for lease
    freeBookInstance = BookInstance.objects.filter(
        reservation__isnull=True,
        book=book
    )

    ratingScore = 0
    if request.user.is_authenticated:
        rating = Rating.objects.filter(book=book, user=request.user)
        if rating:
            ratingScore = rating[0].rating
            
    return render(request, 'book_detail.html', {
        'book': book,
        'userHasReservation': userHasReservation,
        "freeBookInstance": freeBookInstance,
        "checkedStars": range(ratingScore),
        "uncheckedStars": range(ratingScore, 5),
    })


@login_required
@require_POST
def reserveBook(request):
    book_id = request.POST.get('book_id')
    
    # Find book
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Buch existiert nicht.'})

    # Check that each user just reserves one instance
    bookedInstance = BookInstance.objects.filter(book=book, reservation__user=request.user).exists()

    if bookedInstance:
        return JsonResponse({'success': False, 'message': 'Bereits reserviert.'})
    
    # Check if there is an available BookInstance that is not already reserved
    available_instance = BookInstance.objects.filter(book=book, reservation__isnull=True).first()
    
    if not available_instance:
        return JsonResponse({'success': False, 'message': 'Keine verfügbaren Exemplare.'})

    # Create a reservation for this book instance
    reservation = Reservation.objects.create(
        bookInstance=available_instance,
        isActive=True,
        user=request.user
    )
    
    return JsonResponse({'success': True, 'message': 'Buch erfolgreich reserviert.'})



@login_required
@require_POST
def giveRating(request):
    book_id = request.POST.get('book_id')
    star = request.POST.get('star')
    
    # Find book
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Buch existiert nicht.'})

    try:
        star = int(star) + 1 # Cast it to an int to check the validity of the value
    except:
        return JsonResponse({"success": False, "message": "Wrong format of star name"})

    rating, _ = Rating.objects.get_or_create(book=book, user=request.user)
    rating.rating = star
    rating.save()
    
    return JsonResponse({'success': True, 'message': ''})