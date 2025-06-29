"""
URL configuration for book_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from book_shelf.views import *


urlpatterns = [
    path('', login_page, name='login_page'),
    path('books/', books, name='books'),
    path('register/', register, name='register'),
    path('book-list/', book_list, name='book_list'),


    path('delete-book-confirm/<int:id>/', confirm_delete_book, name='confirm_delete_book'),
    path('delete-book/<int:id>/confirm/', delete_book_confirmed, name='delete_book_confirmed'),


    path('update-books/<int:id>/', update_books, name='update_books'),
    path('logout/', logout_page, name='logout_page'),
    path('admin/', admin.site.urls),
    path('reset-password/', reset_password_by_username, name='reset_password_by_username'),


]
