from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Book, News, Profile
from django.contrib.auth.models import User

@receiver(post_save, sender=Book)
def create_news_for_new_book(sender, instance, created, **kwargs):
    if created:
        News.objects.create(title=f'New book added: {instance.title}', content=f'Check out the new book "{instance.title}" by {instance.author}.')


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()