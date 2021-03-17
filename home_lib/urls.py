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
    BookCreateManuallyView
)

urlpatterns = [
    path('', views.home, name='home'),
    path('book/new', BookCreateOptionsView.as_view(), name='book-create-options'),
    #path('book/list', BookListView.as_view(), name='book-list'),
    path('book/search', BookSearchView.as_view(), name='book-search'),
    path('book/read', BookReadView.as_view(), name='book-read'),
    path('book/<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'),
    #path('book/read/<int:pk>/unmark/', BookReadDeleteView.as_view(), name='book-read-unmark'),
    path('book/<int:pk>/mark', BookMarkReadView.as_view(), name='book-mark'),
    path('book/wishlist', BookWishlistView.as_view(), name='book-wishlist'),
    path('book/create-by-isbn/', BookCreateByIsbnView.as_view(), name='book-create-by-isbn'),
    path('book/enter-isbn/', views.BookEnterIsbnView.as_view(), name='book-enter-isbn'),
    path('book/create-manually', views.BookCreateManuallyView.as_view(), name='book-create-manually'),
]
