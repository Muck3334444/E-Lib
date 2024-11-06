from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from ELib.forms import SignupForm
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from django.http import JsonResponse
from library.models import Book
from django.db.models import Q

def signupView(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the new user
            login(request, user)  # Automatically log in the user
            messages.success(request, 'Account created successfully!')
            return redirect('library')  # Redirect to the home page or another page
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})


def logoutView(request):
    if request.method == 'POST':
        # If user confirms logout, call the built-in LogoutView
        return LogoutView.as_view()(request)
    
    # If not POST, just render the confirmation page
    return render(request, 'logout.html')

@login_required
@require_GET
def search_books(request):
    searchBar_input = request.GET.get('searchBar_input', None)

    if searchBar_input: 
        try:
            inputparam = request.GET.get('searchBar_input', '')  # Wert vom Query-Parameter holen
            books = Book.objects.filter(Q(title__icontains=inputparam) | Q(isbn__icontains=inputparam))[:5]  # LIMIT 5
            result = [
                    {
                        'title': book.title, 
                        'isbn': book.isbn, 
                        'image_url': book.image.url if book.image else None,
                        'book_id': book.pk
                    } for book in books
                ]

            if books.exists():
                return JsonResponse({
                    'success': True, 
                    'message': 'Es wurden Bücher zu der Suchanfrage gefunden.',
                    'books': result 
                })
            else:
                return JsonResponse({'success': False, 'message': 'Es gibt keine Bücher zu der Sucheingabe.'})
        except Book.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Fehler beim Datenbank aufruf.'})

    return JsonResponse({'success': False, 'message': 'Es wurde kein Query-Parameter übergeben.'})