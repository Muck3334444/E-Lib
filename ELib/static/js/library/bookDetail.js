function reserve(bookId) {
    $.ajax({
        url: "{% url 'reserve_book' %}",
        type: 'POST',
        data: {
            'book_id': bookId,  // Send the book ID to the backend
            'csrfmiddlewaretoken': '{{ csrf_token }}',  // CSRF token for security
        },
        success: function(response) {
            if (response.success) {
                alert("Buch erfolgreich reserviert!");
            } else {
                alert("Fehler: " + response.message);
            }
        },
        error: function(xhr, status, error) {
            alert("Es ist ein Fehler aufgetreten. Bitte versuchen Sie es erneut.");
        }
    });
}