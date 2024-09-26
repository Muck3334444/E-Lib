"""
All Models concerning Books
"""

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Book(models.Model):
    """
    One logic instance of a book
    """
    title = models.CharField(max_length=256)
    isbn = models.CharField(max_length=32)
    summary = models.TextField()
    author = models.ManyToManyField("Author")
    language = models.ManyToManyField("Language")
    language = models.ManyToManyField("Genre")
    price = models.FloatField()

    def __str__(self) -> str:
        return self.title


class BookInstance(models.Model):
    """
    Describes the physical instance of a book
    """
    uniqueId = models.CharField(max_length=64, unique=True)
    imprint = models.CharField(max_length=512)
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True) # If the book is deleted we still want to know that it existed for a history
    
    def __str__(self) -> str:
        return self.uniqueId
    

class Lease(models.Model):
    """
    Describes what book is leased by whom, when and if it is returned
    """
    bookInstance = models.ForeignKey(BookInstance, on_delete=models.CASCADE, null=True)
    dueBack = models.DateField(null=True)
    returnDate = models.DateField(null=True)
    leaseDate = models.DateTimeField(auto_now_add=True)

class Rating(models.Model):
    """
    Describes a rating on the scale of 1 to 5 a user gave a specific book
    """
    rating = models.IntegerField(validators=[
            MaxValueValidator(5), # Max allowed value is 5 stars
            MinValueValidator(1) # Min is 1
        ])
    bookInstance = models.ForeignKey(Book, on_delete=models.CASCADE)


class Reservation(models.Model):
    """
    Describes the reservation of a specific instance of a book from a certain user
    """
    bookInstance = models.ForeignKey(BookInstance, on_delete=models.CASCADE)
    creationDate = models.DateTimeField(auto_now_add=True)
    isActive = models.BooleanField(default=False)


class Language(models.Model):
    """
    Describes the language a book is written in
    """
    name = models.CharField(max_length=128)

    def __str__(self) -> str:
        return self.name
    

class Author(models.Model):
    """
    Describes an Author
    """
    name = models.CharField(max_length=256)
    dateOfBirth = models.DateField(null=True) # Even though every author has a birthdate it is not always known
    dateOfDeath = models.DateField(null=True)

    def __str__(self) -> str:
        return self.name


class Genre(models.Model):
    """
    Describes the possible Genre
    """
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=512)

    def __str__(self) -> str:
        return self.name
