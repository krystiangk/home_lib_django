from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, ListView, DeleteView, UpdateView, FormView
from .models import Book, Wishlist
from .forms import BookCreateForm, BookSearchForm, BookMarkReadForm, BookWishlistForm, BookIsbnForm
from django.views.generic.edit import FormMixin
from django.db.models import Q
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import find_by_isbn_open_library
from django.contrib import messages
from django.core.exceptions import NON_FIELD_ERRORS


def home(request):
    return render(request, 'home_lib/home.html', {'sidebar': 1})


class BookCreateOptionsView(LoginRequiredMixin, ListView):
    model = Book
    paginate_by = 10
    template_name = 'home_lib/book_create_options.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.model.objects.filter(created_by=self.request.user).order_by('id')
        p = Paginator(queryset, self.paginate_by)
        page_num = self.request.GET.get('page')
        context['number_of_pages'] = p.num_pages
        if page_num:
            context['page_obj'] = p.get_page(page_num)
        else:
            context['page_obj'] = p.get_page(1)
        # Sidebar flag added to change rendering of template messages, to not allow the
        # sidebar to be pushed down by alert messages. Logic implemented in 'base.html'
        context['sidebar'] = 1
        return context


class BaseBookCreateView(CreateView):
    model = Book
    form_class = BookCreateForm

    def form_invalid(self, form):
        if form.has_error(NON_FIELD_ERRORS, 'exists'):
            messages.error(self.request, "This book already exists in the database.")
            return redirect('book:book-create-options')
        return super().form_invalid(form)

    def form_valid(self, form):
        book = form.save(commit=False)
        book.created_by = self.request.user
        book.save()
        return super().form_valid(form)


class BookCreateManuallyView(LoginRequiredMixin, BaseBookCreateView):
    template_name = 'home_lib/book_create_manually.html'


class BookCreateByIsbnView(LoginRequiredMixin, BaseBookCreateView):
    def get(self, *args, **kwargs):
        try:
            if 'isbn13' in self.request.GET:
                isbn = self.request.GET['isbn13']
                print(isbn)
                book = find_by_isbn_open_library(isbn)
                form = BookCreateForm(initial={'title': book['title'], 'author': book['authors'],
                                               'year': book['year'], 'language': book['language']})
                return render(self.request, 'home_lib/book_create_by_isbn.html', {'book': book, 'form': form})
        except KeyError:
            messages.info(self.request, "Sorry, this book has not been found in our databases, but you can still add it manually.")
            return redirect('book:book-enter-isbn')


class BookEnterIsbnView(LoginRequiredMixin, FormView):
    form_class = BookIsbnForm
    template_name = 'home_lib/book_enter_isbn.html'


class BookSearchView(LoginRequiredMixin, FormMixin, ListView):
    form_class = BookSearchForm
    model = Book
    paginate_by = 10
    template_name = 'home_lib/book_search.html'

    def get_queryset(self):
        query = self.request.GET
        object_list = self.model.objects.filter(created_by=self.request.user)
        if query:
            cleaned_query = {k: v for k, v in query.items() if v != ''}
            if cleaned_query.get('submit_button'):
                cleaned_query.pop("submit_button")
            if cleaned_query.get('page'):
                cleaned_query.pop("page")
            or_condition = Q()
            for key, value in cleaned_query.items():
                or_condition.add(Q(**{f'{key}__icontains': value}), Q.OR)
            object_list = Book.objects.filter(or_condition).filter(created_by=self.request.user)
        return object_list


class BookReadView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'home_lib/book_read.html'
    paginate_by = 10

    def get_queryset(self):
        object_list = Book.objects.filter(read=True).filter(created_by=self.request.user)
        return object_list


class BookDeleteView(LoginRequiredMixin, DeleteView):
    model = Book

    def get_success_url(self):
        return reverse('book:book-search')


class BookMarkReadView(LoginRequiredMixin, UpdateView):
    model = Book
    form_class = BookMarkReadForm
    template_name = 'home_lib/book_mark.html'

    def post(self, request, *args, **kwargs):
        super().post(self, request, *args, **kwargs)
        obj = self.model.objects.get(pk=self.kwargs.get('pk'))
        obj.read = not obj.read
        obj.save()
        return redirect('book:book-search')

    def get_success_url(self):
        return reverse('book:book-search')


class BookWishlistDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "home_lib/book_confirm_delete.html"
    model = Wishlist

    def get_success_url(self):
        return reverse('book:book-wishlist')


class BookWishlistView(LoginRequiredMixin, CreateView):
    form_class = BookWishlistForm
    model = Wishlist
    template_name = 'home_lib/book_wishlist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_list"] = self.model.objects.filter(created_by=self.request.user)
        return context

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)



