from django.test import TestCase
from django.contrib.auth.models import User
from books.models import Book, Comment, News,Favorite, Profile, ReadStatus
from datetime import date

class BookModelTestCase(TestCase):
    def test_book_creation(self):
        user = User.objects.create_user(username='testuser', password='12345')
        book = Book.objects.create(title='Test Book', author='Test Author', added_by=user)
        self.assertEqual(book.title, 'Test Book')
        self.assertEqual(book.author, 'Test Author')
        self.assertEqual(book.added_by, user)

class CommentModelTestCase(TestCase):
    def test_comment_creation(self):
        user = User.objects.create_user(username='testuser', password='12345')
        book = Book.objects.create(title='Test Book', author='Test Author', added_by=user)
        comment = Comment.objects.create(user=user, book=book, text='Test Comment')
        self.assertEqual(comment.user, user)
        self.assertEqual(comment.book, book)
        self.assertEqual(comment.text, 'Test Comment')

class NewsModelTestCase(TestCase):
    def test_news_creation(self):
        news = News.objects.create(title='Test News', content='Test Content')
        self.assertEqual(news.title, 'Test News')
        self.assertEqual(news.content, 'Test Content')

class FavoriteModelTestCase(TestCase):
    def test_favorite_creation(self):
        user = User.objects.create_user(username='testuser', password='12345')
        book = Book.objects.create(title='Test Book', author='Test Author', added_by=user)
        favorite = Favorite.objects.create(user=user, book=book)
        self.assertEqual(favorite.user, user)
        self.assertEqual(favorite.book, book)

class ProfileModelTestCase(TestCase):
    def test_profile_creation(self):
        user = User.objects.create_user(username='testuser', password='12345')
        Profile.objects.filter(user=user).delete()
        profile, created = Profile.objects.get_or_create(user=user, defaults={
            'bio': 'Test Bio',
            'location': 'Test Location',
            'birth_date': date(2000, 1, 1)
        })
        self.assertTrue(created)
        self.assertEqual(profile.user, user)
        self.assertEqual(profile.bio, 'Test Bio')
        self.assertEqual(profile.location, 'Test Location')
        self.assertEqual(profile.birth_date, date(2000, 1, 1))


class ReadStatusModelTestCase(TestCase):
    def test_read_status_creation(self):
        user = User.objects.create_user(username='testuser', password='12345')
        book = Book.objects.create(title='Test Book', author='Test Author', added_by=user)
        read_status = ReadStatus.objects.create(user=user, book=book, is_read=True)
        self.assertEqual(read_status.user, user)
        self.assertEqual(read_status.book, book)
        self.assertTrue(read_status.is_read)