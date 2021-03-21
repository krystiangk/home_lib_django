from django.test import TestCase, SimpleTestCase
from ..forms import BookCreateForm, BookSearchForm, BookMarkReadForm
from django.contrib.auth.models import User
from ..models import Book
from django.utils import timezone


class TestBookCreateForm(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('tom', 'tom@tom.com', password='testpass1')
        self.form_data = {
            'title': 'Heat Transfer',
            'author': 'Yunus Cengel',
            'year': 2000,
            'language': 'en',
            'created_by': self.user
        }

    def test_book_create_form_valid_data(self):
        form = BookCreateForm(data=self.form_data)

        self.assertTrue(form.is_valid())

    def test_book_create_form_invalid_data(self):
        form = BookCreateForm(data={})
        self.assertFalse(form.is_valid())
        # 4 errors due to missing form data, and one due to Key Error coming from clean function
        self.assertEquals(len(form.errors), 5)

    def test_book_failed_creation_of_duplicate_book(self):
        Book.objects.create(**self.form_data)
        form = BookCreateForm(data=self.form_data)

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)


class TestBookSearchForm(SimpleTestCase):

    def setUp(self):
        self.form_data = {
            'title': 'Heat Transfer',
            'author': 'Yunus Cengel',
            'year': 2000,
            'language': 'en',
        }

    def test_book_search_form_all_fields_filled(self):
        form = BookSearchForm(data=self.form_data)

        self.assertTrue(form.is_valid())

    def test_book_search_form_no_fields_filled(self):
        form = BookSearchForm(data={})

        self.assertTrue(form.is_valid())


class TestBookMarkReadForm(SimpleTestCase):

    def test_book_mark_read_form_valid_data(self):
        form = BookMarkReadForm(data={'read_timestamp': timezone.now()})

        self.assertTrue(form.is_valid())

    def test_book_mark_read_form_invalid_data(self):
        form = BookMarkReadForm(data={})

        self.assertFalse(form.is_valid())

