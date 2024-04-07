"""
URL configuration for book_store project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from books import views as book_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', book_views.register, name='register'),
    path('login/', book_views.user_login, name='login'),
    path('logout/', book_views.user_logout, name='logout'),
    path('', book_views.home, name='home'),
    path('favorites/', book_views.favorite_books, name='favorites'),
    path('catalog/', book_views.book_catalog, name='catalog'),
    path('books/remove_from_favorites/<int:book_id>/', book_views.remove_from_favorites, name='remove_from_favorites'),
    path('books/add_to_favorites/<int:book_id>/', book_views.add_to_favorites, name='add_to_favorites'),
    path('edit_profile/', book_views.edit_profile, name='edit_profile'),
    path('profile/', book_views.view_profile, name='profile'),
    path('books/<int:book_id>/', book_views.book_detail, name='book_detail'),

]
