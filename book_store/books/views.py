from django.shortcuts import render, redirect,get_object_or_404
from .forms import RegisterForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from .models import Book, Favorite, News,Profile,ReadStatus
from django.contrib import messages
from .forms import UserForm, ProfileForm, CommentForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
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
    query = request.GET.get('q', '')
    message = None

    if query:
        books = Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query))
        message = f"Found {books.count()} books matching your query."
    else:
        books = Book.objects.all()

    if request.user.is_authenticated:
        favorite_books = {fav.book.id: fav for fav in request.user.favorite_set.all()}
        read_statuses = {status.book.id: status.is_read for status in ReadStatus.objects.filter(user=request.user)}
    else:
        favorite_books = {}
        read_statuses = {}

    for book in books:
        book.is_favorite = book.id in favorite_books
        book.is_read = read_statuses.get(book.id, False)
        book.favorite_id = favorite_books.get(book.id, {}).id if book.is_favorite else None

    return render(request, 'books/catalog.html', {'books': books, 'message': message})

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
            messages.success(request, 'The book has been removed from favorites.')
        else:
            messages.info(request, 'Book not found in favorites.')
        return redirect('favorites')
    else:
        return redirect('login')


def edit_profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Information successfully changed')
            return redirect('profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)

    return render(request, 'books/edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})


def view_profile(request):
    return render(request, 'books/view_profile.html')

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    comments = book.comments.all()
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.book = book
            new_comment.user = request.user
            new_comment.save()
            return redirect('book_detail', book_id=book.id)
    else:
        comment_form = CommentForm()
    return render(request, 'books/book_detail.html', {'book': book, 'comments': comments, 'new_comment': new_comment, 'comment_form': comment_form})

def mark_as_read(request, book_id):
    if request.user.is_authenticated:
        book = get_object_or_404(Book, id=book_id)
        ReadStatus.objects.update_or_create(user=request.user, book=book, defaults={'is_read': True})
        return redirect('catalog')
    else:
        return redirect('login')


def mark_as_unread(request, book_id):
    if request.user.is_authenticated:
        book = get_object_or_404(Book, id=book_id)
        ReadStatus.objects.update_or_create(user=request.user, book=book, defaults={'is_read': False})
        return redirect('catalog')
    else:
        return redirect('login')

def view_user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'books/view_profile.html', {'user': user})