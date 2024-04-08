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

from books.views import book_list
from books.views import news_list
from books.views import book_comments

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework import permissions
schema_view = get_schema_view(
    openapi.Info(
        title="BooksStore API",
        default_version='v1',
        description="API description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="admin@admin.ru"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
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
    path('mark_as_read/<int:book_id>/', book_views.mark_as_read, name='mark_as_read'),
    path('mark_as_unread/<int:book_id>/', book_views.mark_as_unread, name='mark_as_unread'),
    path('user_profile/<int:user_id>/', book_views.view_user_profile, name='view_user_profile'),
    path('api/books/', book_list, name='book-list'),
    path('api/news/', news_list, name='news-list'),
    path('api/books/<int:book_id>/comments/', book_comments, name='book-comments'),

]
