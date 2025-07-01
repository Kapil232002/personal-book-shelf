from django.shortcuts import render, redirect
from .models import Book
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

@login_required
def suggest_username(request):
    query = request.GET.get('q', '').lower()
    
    if len(query) >= 3:
        users = User.objects.filter(username__icontains=query).exclude(is_superuser=True)[:10]
        results = [{'username': user.username} for user in users]
        return JsonResponse(results, safe=False)

    return JsonResponse([], safe=False)


@login_required(login_url='/')
def books(request):
    if request.method == "POST":
        data = request.POST
        title = data.get('title')
        author_name = data.get('author_name')
        description = data.get('description')
        reference_link = data.get('reference_link')

        Book.objects.create(
            title=title,
            author=author_name,
            description=description,
            added_by=request.user,
            reference_link=reference_link
        )
        messages.info(request, 'Book registered successfully')
        return redirect('books')

    context = {'page': 'Add Books'}
    return render(request, 'book.html', context)

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Invalid Username')
            return redirect('/')

        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, 'Invalid password')
            return redirect('/')
        else:
            login(request, user)
            return redirect('books')

    return render(request, 'login.html', {'page': 'SignIn'})

def register(request):
    if request.method == "POST":
        data = request.POST
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        username = data.get('username')
        password = data.get('password')

        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username already exists')
            return redirect('/register')

        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username
        )
        user.set_password(password)
        user.save()
        return redirect('/')

    return render(request, 'register.html', {'page': 'SignUp'})

@login_required(login_url='/')
def book_list(request):
    query = request.GET.get('q')

    if request.user.is_staff or request.user.is_superuser:
        books = Book.objects.all()
    else:
        books = Book.objects.filter(added_by=request.user)

    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(description__icontains=query)
        )

    return render(request, 'book_list.html', {'books': books, 'page': 'Book_list'})

@login_required(login_url='/')
def confirm_delete_book(request, id):
    book = Book.objects.get(id=id)
    return render(request, 'confirm.html', {'book': book})

@login_required(login_url='/')
def delete_book_confirmed(request, id):
    book = Book.objects.get(id=id)
    if request.user == book.added_by or request.user.is_staff:
        book.delete()
    else:
        messages.error(request, "You don't have permission to delete this book.")
    return redirect('book_list')

@login_required(login_url='/')
def update_books(request, id):
    book = Book.objects.get(id=id)

    if book.added_by != request.user and not request.user.is_staff:
        messages.error(request, "You're not allowed to edit this book.")
        return redirect('book_list')

    if request.method == "POST":
        data = request.POST
        book.title = data.get('title')
        book.author = data.get('author_name')
        book.description = data.get('description')
        book.reference_link = data.get('reference_link')
        book.save()
        return redirect('book_list')

    return render(request, 'update_book.html', {'books': book, 'page': 'update_book'})

def logout_page(request):
    logout(request)
    return redirect('login_page')

@login_required
def reset_password_by_username(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')

        user = authenticate(request, username=username, password=old_password)
        if user:
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Password changed successfully.')
            return redirect('/')
        else:
            messages.error(request, 'Old password is incorrect or username not found.')

    return render(request, 'reset_password.html')