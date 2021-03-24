from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import (home, BookCreateManuallyView, BookSearchView, BookReadView,
                     BookDeleteView, BookMarkReadView, BookWishlistView)


class TestUrls(SimpleTestCase):

    def test_home_url_resolves(self):
        url = reverse('book:home')
        self.assertEqual(resolve(url).func, home)

    def test_book_create_url_resolves(self):
        url = reverse('book:book-create-manually')
        self.assertEqual(resolve(url).func.view_class, BookCreateManuallyView)

    def test_book_search_url_resolves(self):
        url = reverse('book:book-search')
        self.assertEqual(resolve(url).func.view_class, BookSearchView)

    def test_book_read_url_resolves(self):
        url = reverse('book:book-read')
        self.assertEqual(resolve(url).func.view_class, BookReadView)

    def test_book_delete_url_resolves(self):
        url = reverse('book:book-delete', kwargs={'pk': 5})
        self.assertEqual(resolve(url).func.view_class, BookDeleteView)

    def test_book_mark_url_resolves(self):
        url = reverse('book:book-mark', kwargs={'pk': 5})
        self.assertEqual(resolve(url).func.view_class, BookMarkReadView)

    def test_book_wishlist_url_resolves(self):
        url = reverse('book:book-wishlist')
        self.assertEqual(resolve(url).func.view_class, BookWishlistView)