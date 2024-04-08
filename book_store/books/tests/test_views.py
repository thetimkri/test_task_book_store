from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from books.models import Book, Comment, Favorite, News, Profile, ReadStatus
from django.utils import timezone

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.book = Book.objects.create(title='Test Book', author='Test Author', added_by=self.user)
        self.comment = Comment.objects.create(user=self.user, book=self.book, text='Test Comment')
        self.favorite = Favorite.objects.create(user=self.user, book=self.book)
        self.news = News.objects.create(title='Test News', content='Test Content', date_posted=timezone.now())
        self.profile, _ = Profile.objects.get_or_create(user=self.user)
        self.profile.bio = 'Test Bio'
        self.profile.location = 'Test Location'
        self.profile.birth_date = timezone.now()
        self.profile.save()
    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/register.html')

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/login.html')

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/home.html')

    def test_favorite_books_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('favorites'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/favorites.html')

    def test_book_catalog_view(self):
        response = self.client.get(reverse('catalog'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/catalog.html')

    def test_add_to_favorites_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('add_to_favorites', args=[self.book.id]))
        self.assertEqual(response.status_code, 302)  # Redirect to catalog page after adding to favorites

    def test_remove_from_favorites_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('remove_from_favorites', args=[self.book.id]))
        self.assertEqual(response.status_code, 302)  # Redirect to favorites page after removing from favorites

    def test_edit_profile_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('edit_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/edit_profile.html')

    def test_view_profile_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/view_profile.html')

    def test_book_detail_view(self):
        response = self.client.get(reverse('book_detail', args=[self.book.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/book_detail.html')

    def test_mark_as_read_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('mark_as_read', args=[self.book.id]))
        self.assertEqual(response.status_code, 302)  # Redirect to catalog page after marking as read

    def test_mark_as_unread_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('mark_as_unread', args=[self.book.id]))
        self.assertEqual(response.status_code, 302)  # Redirect to catalog page after marking as unread

    def test_view_user_profile_view(self):
        response = self.client.get(reverse('view_user_profile', args=[self.user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/view_profile.html')

    def test_book_list_api_view(self):
        response = self.client.get(reverse('book-list'))
        self.assertEqual(response.status_code, 200)

    def test_news_list_api_view(self):
        response = self.client.get(reverse('news-list'))
        self.assertEqual(response.status_code, 200)

    def test_book_comments_api_view(self):
        response = self.client.get(reverse('book-comments', args=[self.book.id]))
        self.assertEqual(response.status_code, 200)
