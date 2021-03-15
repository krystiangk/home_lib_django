from django.urls import path
from home_lib import views
from .views import (
    BookCreateView,
    BookSearchView,
    BookReadView,
    BookDeleteView,
    BookMarkReadView,
    BookWishlistView
)

urlpatterns = [
    path('book/home', views.home, name='home'),
    path('book/new', BookCreateView.as_view(), name='book-create'),
    #path('book/list', BookListView.as_view(), name='book-list'),
    path('book/search', BookSearchView.as_view(), name='book-search'),
    path('book/read', BookReadView.as_view(), name='book-read'),
    path('book/<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'),
    #path('book/read/<int:pk>/unmark/', BookReadDeleteView.as_view(), name='book-read-unmark'),
    path('book/<int:pk>/mark', BookMarkReadView.as_view(), name='book-mark'),
    path('book/wishlist', BookWishlistView.as_view(), name='book-wishlist'),
]
