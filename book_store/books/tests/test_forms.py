from django.test import TestCase
from books.forms import RegisterForm, LoginForm, UserForm, ProfileForm, CommentForm
from django.contrib.auth.models import User
from books.models import Profile, Comment, Book
from datetime import date

class TestForms(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser', email='test@example.com')
        self.profile, _ = Profile.objects.get_or_create(user=self.user)
        self.book = Book.objects.create(title='Test Book', author='Test Author', added_by=self.user)

    def test_register_form_valid_data(self):
        form = RegisterForm(data={
            'username': 'newtestuser',
            'email': 'test@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword'
        })
        self.assertTrue(form.is_valid(), form.errors)

    def test_register_form_invalid_data(self):
        form = RegisterForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)

    def test_login_form_valid_data(self):
        form = LoginForm(data={
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertTrue(form.is_valid())

    def test_login_form_invalid_data(self):
        form = LoginForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)

    def test_user_form_valid_data(self):
        form = UserForm(instance=self.user, data={
            'username': 'testuser2',
            'email': 'test2@example.com'
        })
        self.assertTrue(form.is_valid())

    def test_user_form_invalid_data(self):
        form = UserForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)

    def test_profile_form_valid_data(self):
        form = ProfileForm(instance=self.profile, data={
            'bio': 'Test bio',
            'location': 'Test location',
            'birth_date': '2000-01-01'
        })
        self.assertTrue(form.is_valid())

    def test_profile_form_invalid_data(self):
        form = ProfileForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)

    def test_comment_form_valid_data(self):
        form = CommentForm(data={
            'user': self.user.id,
            'book': self.book.id,
            'text': 'Test comment'
        })
        self.assertTrue(form.is_valid())

    def test_comment_form_invalid_data(self):
        form = CommentForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)
