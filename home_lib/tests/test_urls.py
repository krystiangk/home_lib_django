from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import home, BookCreateView, BookSearchView


class TestUrls(SimpleTestCase):

    def test_home_url_resolves(self):
        url = reverse('home')
        print(resolve(url))
        self.assertEqual(resolve(url).func, home)

    def test_book_create_url_resolves(self):
        url = reverse('book-create')
        print(resolve(url))
        self.assertEqual(resolve(url).func.view_class, BookCreateView)

    def test_book_search_url_resolves(self):
        url = reverse('book-search')
        print(resolve(url))
        self.assertEqual(resolve(url).func.view_class, BookSearchView)