from django.db import models
from django.utils import timezone
from datetime import timedelta


class Book(models.Model):
    bookID = models.IntegerField()
    title = models.CharField(max_length=200)
    authors = models.CharField(max_length=100)
    average_rating = models.DecimalField(max_digits=5,decimal_places=2)
    isbn = models.CharField(max_length=13, unique=True)
    num_pages = models.IntegerField()
    publisher = models.CharField(max_length=200)

    def __str__(self):
        return self.title
    

class IssuedBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)  # Assume user is an authenticated user
    issue_date = models.DateTimeField(default=timezone.now)
    return_date = models.DateTimeField(null=True, blank=True)

    def due_date(self):
        return self.issue_date + timedelta(weeks=2)

    def calculate_fine(self):
        
        if self.return_date and self.return_date > self.due_date():
            days_late = (self.return_date - self.due_date()).days
            return days_late * 50  # 50 rupees per day
        return 0

    class Meta:
        ordering = ['-issue_date']  # Order by newest first
