from django.urls import path
from home_lib import views
from .views import (
    BookCreateOptionsView,
    BookSearchView,
    BookReadView,
    BookDeleteView,
    BookMarkReadView,
    BookWishlistView,
    BookCreateByIsbnView,
    BookCreateManuallyView,
    BookWishlistDeleteView,
)

app_name = 'book'

urlpatterns = [
    path('', views.home, name='home'),
    path('new/', BookCreateOptionsView.as_view(), name='book-create-options'),
    path('search/', BookSearchView.as_view(), name='book-search'),
    path('read/', BookReadView.as_view(), name='book-read'),
    path('<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'),
    path('<int:pk>/mark/', BookMarkReadView.as_view(), name='book-mark'),
    path('wishlist/', BookWishlistView.as_view(), name='book-wishlist'),
    path('wishlist/<int:pk>/delete', BookWishlistDeleteView.as_view(), name='book-wishlist-delete'),
    path('create-by-isbn/', BookCreateByIsbnView.as_view(), name='book-create-by-isbn'),
    path('enter-isbn/', views.BookEnterIsbnView.as_view(), name='book-enter-isbn'),
    path('create-manually/', views.BookCreateManuallyView.as_view(), name='book-create-manually'),
]
