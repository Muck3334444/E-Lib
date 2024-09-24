"""
All Models concerning Books
"""

from django.db import models

class Book(models.Model):
    """
    One logic instance of a book
    """
    title = models.CharField(max_length=256)
    isbn = models.CharField(max_length=32)
    summary = models.TextField()
    author = models.ManyToManyField("Author")
    language = models.ManyToManyField("Language")

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
    details = models.CharField(max_length=1024, null=True)
    dueBack = models.DateField(null=True)
    returnDate = models.DateField(null=True)


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
    dateOfBirth = models.DateField()
    dateOfDeath = models.DateField(null=True)

    def __str__(self) -> str:
        return self.name


class Genre(models.Model):
    """
    Describes the possible Genre
    """
    name = models.CharField(max_length=128)

    def __str__(self) -> str:
        return self.name
