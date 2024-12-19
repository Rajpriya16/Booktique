from django.contrib import admin
from .models import Book, IssuedBook

admin.site.register(Book)
admin.site.register(IssuedBook)
