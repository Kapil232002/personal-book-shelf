from django.shortcuts import render,redirect
from .models import *
from django.db.models import Q
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required



# Create your views here.
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
            added_by=request.user,  # ✅ Comma added here
            reference_link=reference_link
        )
        messages.info(request, 'Book registered successfully')
        return redirect('books')

    context = {'page': 'Add Books'}
    return render(request, 'book.html', context)





def login_page(request):
    if request.method =="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username =username).exists():   #check the username in the userlist
            messages.error(request,'Invalid Username')
            return redirect('/')

        user =authenticate(username =username , password =password)   #check the username and password in the database
        if user is None:
            messages.error(request,'Invalid password')
            return redirect('/')
        else:                                 #if after authenticate username and pass will match , it will poss the user otherwise none.
            login(request,user)
            return redirect('books')

    context ={'page':'SignIn'}
    return render(request, 'login.html',context)




def register(request):
    if request.method =="POST":
        data =request.POST
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        username = data.get('username')
        password = data.get('password')

        user =User.objects.filter(username =username)
        if user.exists():
            messages.info(request,'Username already exists')
            return redirect('/register')

        user =User.objects.create(
            first_name = first_name,
            last_name =last_name,
            username =username
        )

        user.set_password(password)
        user.save()
        return redirect('/')
    context ={'page':'SignUp'}
    return render(request, 'register.html',context)
      



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

    # ✅ Show "No books added yet" in template if empty
    # if not books.exists():
    #     messages.info(request, "No books added yet.")

    return render(request, 'book_list.html', {'books': books, 'page': 'Book_list'})






@login_required(login_url ='/')
def delete_book(request, id):
    queryset = Book.objects.get(id =id)
    queryset.delete()
    return redirect('book_list')

@login_required(login_url='/')
def update_books(request, id):
    book = Book.objects.get(id=id)

    if request.method == "POST":
        data = request.POST
        title = data.get('title')
        author_name = data.get('author_name')
        description = data.get('description')
        reference_link = data.get('reference_link')

        username = data.get('added_by')

        user, _ = User.objects.get_or_create(username=username)

        book.title = title
        book.author = author_name
        book.description = description
        book.reference_link = reference_link

        book.added_by = user
        book.save()

        # messages.info(request, 'Updated Successfully')
        return redirect('book_list')  # redirect to list page after update

    context = {'books': book,'page':'update_book'}
    return render(request, 'update_book.html', context)


def logout_page(request):
    logout(request)  # This clears the session
    return redirect('login_page')


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
        else:
            messages.error(request, 'Old password is incorrect or username not found.')

    return render(request, 'reset_password.html')


