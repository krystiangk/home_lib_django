from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from ..views import BookCreateView
from ..models import Book
from django.contrib.auth.models import User


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.user = User.objects.create_user('foo', password='bar', is_superuser=True)
        self.create_book_url = reverse('book-create')
        self.form_data = {
            'title': 'Sapiens',
            'author': 'Harari',
            'year': 1001,
            'language': 'French',
            'created_by': self.user
        }

    def test_home_GET(self):
        response = self.client.get(reverse('home'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'home_lib/home.html')

    def test_book_create_view_GET(self):
        request = self.factory.get('/')
        view = BookCreateView()
        view.setup(request)

        self.assertEquals(1, 1)

    # def test_book_create_view_POST(self):
    #     Book.objects.create(**self.form_data)
    #     self.assertEqual(Book.objects.last().title, "Sapiens")

    def test_post_create_view_POST_success(self):
        user = User.objects.create_user('john', 'lennon@thebeatles.com', is_superuser=True)
        user.set_password('12345')
        user.is_superuser = True
        user.save()

        print('fsdvsdssdv', User.objects.get(id=2))
        self.client.login(username='john', password='12345')
        #force_login(user, backend=None)

        print('bbb')
        print(self.form_data)

        from django.contrib import auth
        user = auth.get_user(self.client)
        if user.is_authenticated:
            print('YEeeeah')



        from django.utils import timezone

        form_data = {
            'title': 'Sapiens',
            'author': 'Harari',
            'year': '1000',
            'language': 'French',
            'created_by': user,
            'entry_timestamp': timezone.now(),
            'read': 'false',
            'read_timestamp': timezone.now()
        }

        import pdb
        pdb.set_trace()
        print(form_data)
        response = self.client.post('/book/new', data=form_data)

        print('aaa')
        self.assertEquals(response.status_code, 200)
        #self.assertEquals(Book.objects.filter(title='Sapiens').count(), 1)

  # def test_create_blog(self): # create update and delete a blog
  #           # log user in and user
  #           self.client.login(username='foo', password='password')
  #
  #           # create new blog
  #           # expected date from the user, you can put invalid data to test from validation
  #           form_data = {
  #               'title': 'new test blog',
  #               'body': 'blog body'
  #           }
  #           form = BlogForm(data=blogform_data) # create form indstance
  #
  #           """
  #           simulate post request with self.client.post
  #           /blog/createblog/ is the url associated with create_blog view
  #           """
  #           response = self.client.post('/blog/createblog/', form_data)
  #           # get number of created blog to be tested later
  #           num_of_blogs = Blog.objects.all().count()
  #           # get created blog
  #           blog = Blog.objects.get(title=form_data['title'])
  #           # test form validation
  #           self.assertTrue(blogform.is_valid())
  #           # test slugify method, if any
  #           self.assertEqual(blog.slug, 'new-test-blog')
  #           # test if the blog auther is the same logged in user
  #           self.assertEqual(blog.author, self.user1)
  #           # one blog created, test if this is true
  #           self.assertEqual(num_of_blogs, 1)
  #           # test redirection after blog created
  #           self.assertRedirects(
  #               createblog_response,
  #               '/blog/new-test-blog/',
  #               status_code=302,
  #               target_status_code=200
  #           )