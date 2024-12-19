from django import forms
from .models import IssuedBook, Book
from django.contrib.auth.models import User

class IssueBookForm(forms.Form):
    bookID = forms.IntegerField(label='Book ID')
    username = forms.CharField(label='Username')

    def clean(self):
        cleaned_data = super().clean()
        bookID = cleaned_data.get('bookID')
        username = cleaned_data.get('username')

        # Check if the book exists
        try:
            book = Book.objects.get(bookID=bookID)
        except Book.DoesNotExist:
            raise forms.ValidationError(f"Book with ID {bookID} does not exist.")
        
        # Check if the user exists
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError(f"User with username {username} does not exist.")

        cleaned_data['book'] = book
        cleaned_data['user'] = user
        return cleaned_data
