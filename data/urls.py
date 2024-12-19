from django.urls import path
from . import views

urlpatterns = [
    path('issue_book/', views.issue_book_view, name='issue_book'),
    path('return_book/', views.return_book_view, name='return_book'),
    path('issued_books/', views.issued_books_view, name='issued_books'),
    path('home/',views.home,name='home'),
    path('issued_books_report/', views.issued_books_report_admin, name='issued_books_report'),
]
