from django.test import TestCase, Client, SimpleTestCase
from django.urls import reverse
from ..models import Book, Wishlist
from django.contrib.auth.models import User
import datetime


class TestHomeView(SimpleTestCase):

    def test_home_GET(self):
        response = self.client.get(reverse('book:home'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'home_lib/home.html')


class TestCreateAndDeleteView(TestCase):

    def setUp(self):
        self.client = Client()
        self.username = 'tom'
        self.password = 'testpass1'
        self.user = User.objects.create_user(self.username, 'tom@tom.com', password=self.password)
        self.client.login(username=self.username, password=self.password)
        self.create_book_url = reverse('book:book-create-manually')

        self.form_data_1 = {
            'title': 'Heat Transfer',
            'author': 'Yunus Cengel',
            'year': 2000,
            'language': 'en',
        }

    def test_book_create_view_GET(self):
        response = self.client.get(self.create_book_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'home_lib/book_create_manually.html')

    def test_book_create_view_POST_success(self):
        response = self.client.post(self.create_book_url, data=self.form_data_1)
        book = Book.objects.last()
        num_of_books = Book.objects.all().count()

        self.assertEquals(num_of_books, 1)

        self.assertEquals(response.status_code, 302)

        self.assertEquals(book.title, 'Heat Transfer')
        self.assertEquals(book.author, 'Yunus Cengel')
        self.assertEquals(book.year, 2000)
        self.assertEquals(book.language, 'en')
        self.assertEquals(book.created_by, self.user)
        self.assertEquals(book.read, False)
        self.assertEquals(book.read_timestamp, None)
        self.assertEquals(type(book.entry_timestamp), datetime.datetime)

        self.assertRedirects(
                response,
                reverse('book:book-create-options'),
                status_code=302,
                target_status_code=200
            )

    def test_delete_view(self):
        self.client.post(self.create_book_url, data=self.form_data_1)
        response = self.client.get(reverse('book:book-create-options'))

        self.assertEquals(len(response.context['page_obj']), 1)

        book = Book.objects.last()
        self.client.post(reverse('book:book-delete', args=(book.id,)), follow=True)
        response = self.client.get(reverse('book:book-create-options'))

        self.assertEquals(len(response.context['page_obj']), 0)

    def test_book_wishlist_create_view_GET(self):
        response = self.client.get(reverse('book:book-wishlist'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'home_lib/book_wishlist.html')


    def test_book_wishlist_view_POST_success(self):
        response = self.client.post(reverse('book:book-wishlist'), data=self.form_data_1)

        book = Wishlist.objects.last()
        num_of_books = Wishlist.objects.all().count()

        self.assertEquals(num_of_books, 1)

        self.assertEquals(response.status_code, 302)

        self.assertEquals(book.title, 'Heat Transfer')
        self.assertEquals(book.author, 'Yunus Cengel')
        self.assertEquals(book.year, 2000)
        self.assertEquals(book.language, 'en')
        self.assertEquals(book.created_by, self.user)
        self.assertEquals(type(book.entry_timestamp), datetime.datetime)

        self.assertRedirects(
                response,
                reverse('book:book-wishlist'),
                status_code=302,
                target_status_code=200
            )


class TestSearchAndReadViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('tom', 'tom@tom.com', password='testpass1')
        self.user_2 = User.objects.create_user('bill', 'bill@deal.com', password='testpass2')
        self.create_book_url = reverse('book:book-create-manually')
        self.search_url = reverse('book:book-search')
        self.read_url = reverse('book:book-read')
        self.form_data_1 = {
            'title': 'Heat Transfer',
            'author': 'Yunus Cengel',
            'year': 2000,
            'language': 'en',
        }
        self.form_data_2 = {
            'title': "L'etranger",
            'author': 'Albert Camus',
            'year': 2000,
            'language': 'fr',
        }
        self.form_data_3 = {
            'title': "Republic",
            'author': 'Plato',
            'year': 2000,
            'language': 'en',
        }
        self.client.login(username='tom', password='testpass1')
        self.client.post(self.create_book_url, data=self.form_data_1)
        self.client.post(self.create_book_url, data=self.form_data_2)
        self.client.post(self.create_book_url, data=self.form_data_3)

    def test_book_search_view_find_by_author_success(self):
        response = self.client.get(self.search_url, {'author': 'yunus'})

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'home_lib/book_search.html')
        self.assertEquals(response.context['object_list'][0].author, 'Yunus Cengel')
        self.assertEquals(len(response.context['object_list']), 1)

    def test_book_search_view_find_by_title_disregard_case_icontains_success(self):
        response = self.client.get(self.search_url, {'title': 'tran'})

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'home_lib/book_search.html')
        self.assertEquals(response.context['object_list'][0].title, 'Heat Transfer')
        self.assertEquals(response.context['object_list'][1].title, "L'etranger")
        self.assertEquals(len(response.context['object_list']), 2)

    def test_book_search_view_find_zero_success(self):
        response = self.client.get(self.search_url, {'title': 'abcd'})

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'home_lib/book_search.html')
        self.assertEquals(len(response.context['object_list']), 0)

    def test_book_search_view_find_by_year_success(self):
        response = self.client.get(self.search_url, {'year': 2000})

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'home_lib/book_search.html')
        self.assertEquals(response.context['object_list'][0].title, 'Heat Transfer')
        self.assertEquals(response.context['object_list'][1].title, "L'etranger")
        self.assertEquals(response.context['object_list'][2].title, "Republic")
        self.assertEquals(len(response.context['object_list']), 3)

    def test_book_search_view_find_by_language_success(self):
        response = self.client.get(self.search_url, {'language': "EN"})

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'home_lib/book_search.html')
        self.assertEquals(response.context['object_list'][0].title, 'Heat Transfer')
        self.assertEquals(response.context['object_list'][1].title, "Republic")
        self.assertEquals(len(response.context['object_list']), 2)

    def test_book_search_view_show_only_books_of_logged_in_user_success(self):
        self.client.login(username='bill', password='testpass2')
        self.client.post(self.create_book_url, data={'title': 'Trzy po trzy',
                                            'author': 'Fredro',
                                            'year': 1880,
                                            'language': 'pl'})

        response = self.client.get(self.search_url)
        self.assertEquals(len(response.context['object_list']), 1)
        self.assertEquals(response.context['object_list'][0].title, 'Trzy po trzy')

    def test_book_read_view(self):
        response = self.client.get(self.read_url)
        self.assertEquals(len(response.context['object_list']), 0)

    def test_book_mark_read_view(self):
        book = Book.objects.get(title="Republic")

        self.client.post(reverse('book:book-mark',  args=(book.id,)))
        response = self.client.get(self.read_url)
        self.assertEquals(len(response.context['object_list']), 1)
