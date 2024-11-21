function search_books() {
    const input = document.getElementById('search_field_searchbar').value;  
    const search_button_searchbar = document.getElementById('search_button_searchbar');
    const search_books_url = search_button_searchbar.getAttribute('data_search_books_url');

    $.ajax({
        url: search_books_url,
        type: 'GET',
        data: {
            'searchBar_input': input
        },
        success: function(response) {
            if (response.success && response.books.length > 0) {
                display_search_result(response.books);
            } else {
                alert("Fehler: " + response.message);
            }
        },
        error: function(jqXHR, status, error) {
            alert("Fehler: " + error.message);
        }
    });
}

function display_search_result(books) {
    const result_Container = document.getElementById('results_container_searchbar');
    result_Container.classList.add('results_container');
    result_Container.innerHTML = '';

    console.log(books);

    books.forEach(book => {
        const book_Block = document.createElement('div');
        book_Block.className = 'book_block';
        book_Block.innerHTML = `
            <h3 class="book_title">${book.title}</h3>
            <p class="book_isbn">ISBN: ${book.isbn}</p>`;
        if (book.image_url) {
            const imgElement = document.createElement("img");
            imgElement.src = book.image_url;
            imgElement.alt = `${book.title} Cover`;
            imgElement.className = "book_image";
            book_Block.appendChild(imgElement);
        }


        const book_detail_link = document.createElement('a');
        book_detail_link.setAttribute('href', book_detail_url_query_param);
        book_detail_link.textContent = 'Details anzeigen';
        book_Block.appendChild(book_detail_link);

        result_Container.appendChild(book_Block);
    });
};