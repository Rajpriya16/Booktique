from django.shortcuts import render, redirect
from .models import IssuedBook
from .forms import IssueBookForm
from django.utils import timezone
from .models import Book
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.db.models import F, Value, Case, When, IntegerField
from datetime import timedelta
from django.utils.timezone import now

from django.core.paginator import Paginator

@login_required(login_url='login')
def home(request):
    query = request.GET.get('q')  # Get the search query from the form
    if query:
        books = Book.objects.filter(
            Q(title__icontains=query) | Q(authors__icontains=query)
        )
    else:
        books = Book.objects.all()  # Get all books

    # Pagination: Show 50 books per page
    paginator = Paginator(books, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'index.html', {'page_obj': page_obj, 'username': request.user.username})



@user_passes_test(lambda u: u.is_superuser)  # Restrict to superusers
def issue_book_view(request):
    if request.method == 'POST':
        form = IssueBookForm(request.POST)
        if form.is_valid():
            book = form.cleaned_data['book']
            user = form.cleaned_data['user']

            # Issue the book to the user
            IssuedBook.objects.create(book=book, user=user)
            #messages.success(request, f"Book '{book.title}' issued to {user.username}.")
            return redirect('home')
    else:
        form = IssueBookForm()

    return render(request, 'issue_book.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)  
def return_book_view(request):
    return_message = ""
    fine = None
    if request.method == 'POST':
        form = IssueBookForm(request.POST)  # Reuse the form for bookID and username
        if form.is_valid():
            book = form.cleaned_data['book']
            user = form.cleaned_data['user']

            try:
                issued_book = IssuedBook.objects.get(book=book, user=user, return_date__isnull=True)
                issued_book.return_date = timezone.now()
                issued_book.save()

                fine = issued_book.calculate_fine()
                #if fine > 0:
                   # messages.warning(request, f"Book returned. Fine due: {fine} rupees.")
                #else:
                    #messages.success(request, "Book returned successfully.")
                #return redirect('home')
            except IssuedBook.DoesNotExist:
                return_message = "No issued book found for the given details, or the book has already been returned."
    else:
        form = IssueBookForm()

    return render(request, 'return_book.html', {'form': form,'fine':fine,'return_message': return_message})


@login_required(login_url='login')
def issued_books_view(request):
    issued_books = IssuedBook.objects.filter(user=request.user).order_by('-issue_date')  # Fetch user's issued books
    return render(request, 'issued_books.html', {'issued_books': issued_books})

@user_passes_test(lambda u: u.is_superuser)
def issued_books_report_admin(request):
    # Fetch issued books for the last 2 months
    two_months_ago = now() - timedelta(days=60)
    recent_books = IssuedBook.objects.filter(issue_date__gte=two_months_ago)

    # Fetch all unreturned books, including those older than 2 months
    unreturned_books = IssuedBook.objects.filter(return_date__isnull=True)

    # Combine both querysets
    books_to_display = recent_books | unreturned_books

    # Prepare data for the template
    books_with_fines = []
    for issued_book in books_to_display:
        fine = issued_book.calculate_fine()
        books_with_fines.append({
            'book_id': issued_book.book.bookID,
            'book_name': issued_book.book.title,
            'username': issued_book.user,  # Get username from IssuedBook's user field
            'issue_date': issued_book.issue_date,
            'return_date': issued_book.return_date,
            'fine': fine,
        })

    # Sort books by issue date (latest first)
    books_with_fines.sort(key=lambda x: x['issue_date'], reverse=True)

    # Render the data to the template
    return render(request, 'issued_books_report.html', {'books': books_with_fines})
