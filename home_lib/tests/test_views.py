from django.test import TestCase, Client, SimpleTestCase
from django.urls import reverse
from ..models import Book, Wishlist
from django.contrib.auth.models import User
import datetime


class TestHomeView(SimpleTestCase):

    def test_home_GET(self):
        response = self.client.get(reverse('home'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'home_lib/home.html')


class TestCreateAndDeleteView(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('tom', 'tom@tom.com', password='testpass1')
        self.create_book_url = reverse('book-create')

        self.form_data_1 = {
            'title': 'Heat Transfer',
            'author': 'Yunus Cengel',
            'year': 1001,
            'language': 'EN',
        }

    def test_book_create_view_GET(self):
        self.client.login(username='tom', password='testpass1')

        response = self.client.get(self.create_book_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'home_lib/book_create.html')

    def test_book_create_view_POST_success(self):
        self.client.login(username='tom', password='testpass1')

        # from django.contrib import auth
        # user_1 = auth.get_user(self.client)
        # if user_1.is_authenticated:
        #     print('user successfully authenticated')

        response = self.client.post('/book/new', data=self.form_data_1)

        book = Book.objects.last()
        num_of_books = Book.objects.all().count()

        self.assertEquals(num_of_books, 1)

        self.assertEquals(response.status_code, 302)

        self.assertEquals(book.title, 'Heat Transfer')
        self.assertEquals(book.author, 'Yunus Cengel')
        self.assertEquals(book.year, 1001)
        self.assertEquals(book.language, 'EN')
        self.assertEquals(book.created_by, self.user)
        self.assertEquals(book.read, False)
        self.assertEquals(book.read_timestamp, None)
        self.assertEquals(type(book.entry_timestamp), datetime.datetime)

        self.assertRedirects(
                response,
                self.create_book_url,
                status_code=302,
                target_status_code=200
            )

    def test_delete_view(self):
        self.client.login(username='tom', password='testpass1')
        self.client.post('/book/new', data=self.form_data_1)
        response = self.client.get('/book/new')

        self.assertEquals(len(response.context['page_obj']), 1)

        book = Book.objects.last()
        self.client.post(reverse('book-delete', args=(book.id,)), follow=True)
        response = self.client.get('/book/new')

        self.assertEquals(len(response.context['page_obj']), 0)

    def test_book_wishlist_create_view_GET(self):
        self.client.login(username='tom', password='testpass1')

        response = self.client.get(reverse('book-wishlist'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'home_lib/book_wishlist.html')


    def test_book_wishlist_view_POST_success(self):
        self.client.login(username='tom', password='testpass1')

        response = self.client.post(reverse('book-wishlist'), data=self.form_data_1)

        book = Wishlist.objects.last()
        num_of_books = Wishlist.objects.all().count()

        self.assertEquals(num_of_books, 1)

        self.assertEquals(response.status_code, 302)

        self.assertEquals(book.title, 'Heat Transfer')
        self.assertEquals(book.author, 'Yunus Cengel')
        self.assertEquals(book.year, 1001)
        self.assertEquals(book.language, 'EN')
        self.assertEquals(book.created_by, self.user)
        self.assertEquals(type(book.entry_timestamp), datetime.datetime)

        self.assertRedirects(
                response,
                reverse('book-wishlist'),
                status_code=302,
                target_status_code=200
            )


class TestSearchAndReadViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('tom', 'tom@tom.com', password='testpass1')
        self.user_2 = User.objects.create_user('bill', 'bill@deal.com', password='testpass2')
        self.search_url = reverse('book-search')
        self.read_url = reverse('book-read')
        self.form_data_1 = {
            'title': 'Heat Transfer',
            'author': 'Yunus Cengel',
            'year': 1001,
            'language': 'EN',
        }
        self.form_data_2 = {
            'title': "L'etranger",
            'author': 'Albert Camus',
            'year': 1001,
            'language': 'FR',
        }
        self.form_data_3 = {
            'title': "Republic",
            'author': 'Plato',
            'year': 1001,
            'language': 'EN',
        }
        self.client.login(username='tom', password='testpass1')
        self.client.post('/book/new', data=self.form_data_1)
        self.client.post('/book/new', data=self.form_data_2)
        self.client.post('/book/new', data=self.form_data_3)

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
        response = self.client.get(self.search_url, {'year': 1001})

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
        self.client.post('/book/new', data={'title': 'Trzy po trzy',
                                            'author': 'Fredro',
                                            'year': 1880,
                                            'language': 'PL'})

        response = self.client.get(self.search_url)
        self.assertEquals(len(response.context['object_list']), 1)
        self.assertEquals(response.context['object_list'][0].title, 'Trzy po trzy')

    def test_book_read_view(self):
        response = self.client.get(self.read_url)
        self.assertEquals(len(response.context['object_list']), 0)

    def test_book_mark_read_view(self):
        book = Book.objects.get(title="Republic")

        self.client.post(reverse('book-mark',  args=(book.id,)))
        response = self.client.get(self.read_url)
        self.assertEquals(len(response.context['object_list']), 1)
