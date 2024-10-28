from django import forms
from .models import Author, Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'isbn', 'price', 'summary', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'dateOfBirth', 'dateOfDeath']
        widgets = {
            'name': forms.DateInput(attrs={'class': 'form-control'}),
            'dateOfBirth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'dateOfDeath': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }