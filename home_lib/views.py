from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from .models import Book
from .forms import BookCreateForm, BookSearchForm
from django.views.generic.edit import FormMixin
from django.db.models import Q
from django.urls import reverse


# Create your views here.
def home(request):
    return render(request, 'home_lib/home.html')


class BookCreateView(CreateView):
    form_class = BookCreateForm
    model = Book
    template_name = 'home_lib/book_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_list"] = self.model.objects.filter(created_by=self.request.user)
        return context

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class BookSearchView(FormMixin, ListView):
    form_class = BookSearchForm
    model = Book
    template_name = 'home_lib/book_search.html'

    def get_queryset(self):
        query = self.request.GET
        object_list = self.model.objects.filter(created_by=self.request.user)
        if query:
            cleaned_query = {k: v for k, v in query.items() if v != ''}
            cleaned_query.pop("submit_button")
            or_condition = Q()
            for key, value in cleaned_query.items():
                or_condition.add(Q(**{f'{key}__icontains': value}), Q.OR)
            object_list = Book.objects.filter(or_condition).filter(created_by=self.request.user)
        return object_list


class BookReadView(ListView):
    model = Book
    template_name = 'home_lib/book_read.html'

    def get_queryset(self):
        object_list = Book.objects.filter(read=True)
        return object_list


class BookDeleteView(DeleteView):
    model = Book

    def get_success_url(self):
        return reverse('book-search')


class BookReadDeleteView(DeleteView):
    model = Book
    template_name = 'home_lib/book_read_delete.html'

    def get_success_url(self):
        return reverse('book-read')


class BookMarkReadView(UpdateView):
    model = Book
    fields = ['read']
    template_name = 'home_lib/book_mark.html'

    def post(self, request, *args, **kwargs):
        obj = self.model.objects.get(pk=self.kwargs.get('pk'))
        obj.read = not obj.read
        obj.save()
        return redirect('book-search')

    def get_success_url(self):
        return reverse('book-search')