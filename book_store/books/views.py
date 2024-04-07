from django.shortcuts import render, redirect,get_object_or_404
from .forms import RegisterForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from .models import Book, Favorite, News
from django.contrib import messages

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'books/register.html', {'form': form})

def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return redirect('login')
    else:
        form = LoginForm()
    return render(request, 'books/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')


def home(request):
    news_feed = News.objects.all().order_by('-date_posted')
    return render(request, 'books/home.html', {'news_feed': news_feed})

def favorite_books(request):
    if request.user.is_authenticated:
        favorites = Favorite.objects.filter(user=request.user)
        return render(request, 'books/favorites.html', {'favorites': favorites})
    else:
        return redirect('login')

def book_catalog(request):
    books = Book.objects.all()
    return render(request, 'books/catalog.html', {'books': books})


def add_to_favorites(request, book_id):

    book = get_object_or_404(Book, id=book_id)
    if request.user.is_authenticated:
        favorite, created = Favorite.objects.get_or_create(user=request.user, book=book)
        if created:
            messages.success(request, 'Tne book add to favorite')
            return redirect('catalog')
        else:
            messages.info(request, 'The book is already in your favorites')
            return redirect('catalog')
    else:
        messages.error(request,'Something went wrong')
        return redirect('login')

def remove_from_favorites(request, book_id):
    if request.user.is_authenticated:
        book = get_object_or_404(Book, id=book_id)
        favorite = Favorite.objects.filter(user=request.user, book=book)
        if favorite.exists():
            favorite.delete()
            messages.success(request, 'Книга удалена из избранного.')
        else:
            messages.info(request, 'Книга не найдена в избранном.')
        return redirect('favorites')
    else:
        return redirect('login')