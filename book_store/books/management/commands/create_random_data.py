from django.core.management.base import BaseCommand
from books.models import Book, Comment,Favorite,ReadStatus
from django.contrib.auth.models import User
from faker import Faker
import random
import logging

logger = logging.getLogger('django')
class Command(BaseCommand):
    help = 'Creates random books, comments, users, and profiles'

    def handle(self, *args, **kwargs):
        self.create_random_users_and_profiles()
        self.create_random_books_and_comments()


    def create_random_users_and_profiles(self):
        fake = Faker()
        for _ in range(15):
            username = fake.user_name()
            email = fake.email()
            password = fake.password()
            user = User.objects.create_user(username=username, email=email, password=password)
            user.profile.bio = fake.text()
            user.profile.location = fake.city()
            user.profile.birth_date = fake.date_of_birth()
            user.save()

            favorite_books_count = random.randint(0, Book.objects.count())
            favorite_books = random.sample(list(Book.objects.all()), favorite_books_count)
            for book in favorite_books:
                Favorite.objects.create(user=user, book=book)

            read_books_count = random.randint(0, Book.objects.count())
            read_books = random.sample(list(Book.objects.all()), read_books_count)
            for book in read_books:
                ReadStatus.objects.create(user=user, book=book, is_read=True)

    logger.info(f"Start command to make Fake Users with Profile")

    def create_random_books_and_comments(self):
        fake = Faker()
        for _ in range(20):
            user = random.choice(User.objects.all())
            book = Book.objects.create(
                title=fake.sentence(nb_words=3),
                author=fake.name(),
                added_by=user
            )
            for _ in range(random.randint(0, 10)):
                commenter = random.choice(User.objects.exclude(pk=user.pk))
                book.comments.create(
                    user=commenter,
                    text=fake.text()
                )

    logger.info(f"Start command to make Fake Books with commenters")
