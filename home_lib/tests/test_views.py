from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from ..views import BookCreateView
from ..models import Book
from django.contrib.auth.models import User
import datetime


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', password='12345')
        self.create_book_url = reverse('book-create')
        self.home_url = reverse('home')

        self.form_data = {
            'title': 'Sapiens',
            'author': 'Harari',
            'year': 1001,
            'language': 'FR',
        }

    def test_home_GET(self):
        response = self.client.get(reverse('home'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'home_lib/home.html')

    def test_book_create_view_GET(self):
        self.client.login(username='john', password='12345')

        response = self.client.get(self.create_book_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'home_lib/book_create.html')

    def test_book_create_view_POST_success(self):
        self.client.login(username='john', password='12345')

        # from django.contrib import auth
        # user_1 = auth.get_user(self.client)
        # if user_1.is_authenticated:
        #     print('user successfully authenticated')

        response = self.client.post('/book/new', data=self.form_data)

        book = Book.objects.last()
        num_of_books = Book.objects.all().count()

        self.assertEquals(num_of_books, 1)

        self.assertEquals(response.status_code, 302)

        self.assertEquals(book.title, 'Sapiens')
        self.assertEquals(book.author, 'Harari')
        self.assertEquals(book.year, 1001)
        self.assertEquals(book.language, 'FR')
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
