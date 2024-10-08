"""
All Models concerning Books
"""

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

class Book(models.Model):
    """
    One logic instance of a book
    """
    title = models.CharField(max_length=256)
    isbn = models.CharField(max_length=32)
    summary = models.TextField(default="")
    author = models.ManyToManyField("Author")
    language = models.ManyToManyField("Language")
    genre = models.ManyToManyField("Genre")
    price = models.FloatField(null=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self) -> str:
        return self.title
    
    @property
    def averageRating(self):
        ratings = self.rating_set.all()
        if len(ratings) == 0:
            return None
        total = 0
        for rating in ratings:
            total += rating.rating
        return round(total / len(ratings),1)
    
    @property
    def languages(self):
        if len(self.language.all()) == 0:
            return "Keine Angaben"
        allLanguages = ""
        for language in self.language.all():
            allLanguages += f"{language.name}, "
        return allLanguages[:-2] # Remove the comma and space from the end
    
    @property
    def genres(self):
        if len(self.genre.all()) == 0:
            return "Keine Angaben"
        allGenres = ""
        for genre in self.genre.all():
            allGenres += f"{genre.name}, "
        return allGenres[:-2] # Remove the comma and space from the end
    
    @property
    def authors(self):
        if len(self.author.all()) == 0:
            return ""
        allAuthors = ""
        for author in self.author.all():
            allAuthors += f"{author.name}, "
        return allAuthors[:-2] # Remove the comma and space from the end


class BookInstance(models.Model):
    """
    Describes the physical instance of a book
    """
    uniqueId = models.CharField(max_length=64, unique=True)
    imprint = models.CharField(max_length=512, default="")
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Rating(models.Model):
    """
    Describes a rating on the scale of 1 to 5 a user gave a specific book
    """
    rating = models.IntegerField(validators=[
            MaxValueValidator(5), # Max allowed value is 5 stars
            MinValueValidator(1) # Min is 1
        ], null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Reservation(models.Model):
    """
    Describes the reservation of a specific instance of a book from a certain user
    """
    bookInstance = models.ForeignKey(BookInstance, on_delete=models.CASCADE)
    creationDate = models.DateTimeField(auto_now_add=True)
    isActive = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


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
    name = models.CharField(max_length=128, unique=True)
    description = models.CharField(max_length=512)

    def __str__(self) -> str:
        return self.name
