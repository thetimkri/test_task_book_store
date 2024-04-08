from django.shortcuts import render, redirect,get_object_or_404
from .forms import RegisterForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from .models import Book, Favorite, News,Profile,ReadStatus
from django.contrib import messages
from .forms import UserForm, ProfileForm, CommentForm
from django.db.models import Q,Count
from django.contrib.auth.models import User
import logging
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Book
from .serializers import BookSerializer,NewsSerializer,CommentSerializer


logger = logging.getLogger('django')
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            logger.info(f"New user registered: {user.username}")
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
                logger.info(f"User logged in: {username}")
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password. Please sign up.")
                logger.warning(f"Failed login attempt for username: {username}")
                return redirect('register')
    else:
        form = LoginForm()
    return render(request, 'books/login.html', {'form': form})

def user_logout(request):
    logger.info(f"User logged out: {request.user.username}")
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
        logger.warning("Unauthorized access to favorite books")
        return redirect('login')

def book_catalog(request):
    query = request.GET.get('q', '')
    message = None

    if query:
        books = Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query))
        message = f"Found {books.count()} books matching your query."
    else:
        books = Book.objects.all()

    books = books.annotate(
        favorites_count=Count('favorite', distinct=True),
        read_count=Count('readstatus', filter=Q(readstatus__is_read=True), distinct=True)
    )

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
            messages.success(request, 'The book has been added to favorites.')
            logger.info(f"Book '{book.title}' added to favorites by {request.user.username}")
        else:
            messages.info(request, 'The book is already in your favorites.')
        return redirect('catalog')
    else:
        logger.warning("Unauthorized attempt to add book to favorites")
        return redirect('login')

def remove_from_favorites(request, book_id):
    if request.user.is_authenticated:
        book = get_object_or_404(Book, id=book_id)
        favorite = Favorite.objects.filter(user=request.user, book=book)
        if favorite.exists():
            favorite.delete()
            messages.success(request, 'The book has been removed from favorites.')
            logger.info(f"Book '{book.title}' removed from favorites by {request.user.username}")
        else:
            messages.info(request, 'Book not found in favorites.')
        return redirect('favorites')
    else:
        logger.warning("Unauthorized attempt to remove book from favorites")
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
            messages.success(request, 'Your profile information has been updated.')
            logger.info(f"User '{request.user.username}' updated their profile")
            return redirect('profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)

    return render(request, 'books/edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})

def view_profile(request):
    logger.info(f"Profile viewed: {request.user.username}")
    return render(request, 'books/view_profile.html')

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    comments = book.comments.all()
    new_comment = None
    if request.method == 'POST':
        if request.user.is_authenticated:
            comment_form = CommentForm(data=request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.book = book
                new_comment.user = request.user
                new_comment.save()
                logger.info(f"New comment added to book '{book.title}' by {request.user.username}")
                return redirect('book_detail', book_id=book.id)
        else:
            messages.error(request, "You must be logged in to post a comment.")
            return redirect('login')
    else:
        comment_form = CommentForm()

    return render(request, 'books/book_detail.html', {
        'book': book,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form
    })

def mark_as_read(request, book_id):
    if request.user.is_authenticated:
        book = get_object_or_404(Book, id=book_id)
        ReadStatus.objects.update_or_create(user=request.user, book=book, defaults={'is_read': True})
        logger.info(f"Book '{book.title}' marked as read by {request.user.username}")
        return redirect('catalog')
    else:
        logger.warning("Unauthorized attempt to mark book as read")
        return redirect('login')

def mark_as_unread(request, book_id):
    if request.user.is_authenticated:
        book = get_object_or_404(Book, id=book_id)
        ReadStatus.objects.update_or_create(user=request.user, book=book, defaults={'is_read': False})
        logger.info(f"Book '{book.title}' marked as unread by {request.user.username}")
        return redirect('catalog')
    else:
        logger.warning("Unauthorized attempt to mark book as unread")
        return redirect('login')

def view_user_profile(request, user_id):
    viewed_user = get_object_or_404(User, id=user_id)
    logger.info(f"User '{request.user.username}' viewed profile of '{viewed_user.username}'")
    return render(request, 'books/view_profile.html', {'user': viewed_user})

@api_view(['GET'])
def book_list(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    logger.info("Book list requested")
    return Response(serializer.data)

@api_view(['GET'])
def news_list(request):
    news = News.objects.all()
    serializer = NewsSerializer(news, many=True)
    logger.info("News list requested")
    return Response(serializer.data)

@api_view(['GET'])
def book_comments(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    comments = book.comments.all()
    serializer = CommentSerializer(comments, many=True)
    logger.info(f"Comments for book {book_id} requested")
    return Response(serializer.data)