from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from .models import Book, Wishlist
from .forms import BookCreateForm, BookSearchForm, BookMarkReadForm, BookWishlistForm
from django.views.generic.edit import FormMixin
from django.db.models import Q
from django.urls import reverse
from django.core.paginator import Paginator

# Create your views here.
def home(request):
    return render(request, 'home_lib/home.html')


class BookCreateView(CreateView):
    model = Book
    paginate_by = 15
    template_name = 'home_lib/book_create.html'
    form_class = BookCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.model.objects.filter(created_by=self.request.user)
        p = Paginator(queryset, self.paginate_by)
        page_num = self.request.GET.get('page')
        if page_num:
            context['page_obj'] = p.get_page(page_num)
        else:
            context['page_obj'] = p.get_page(1)
        return context

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    # def post(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     return super(BookCreateView).post(request, *args, **kwargs)


class BookSearchView(FormMixin, ListView):
    form_class = BookSearchForm
    model = Book
    paginate_by = 15
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


class BookReadView(ListView):
    model = Book
    template_name = 'home_lib/book_read.html'
    paginate_by = 15

    def get_queryset(self):
        object_list = Book.objects.filter(read=True)
        return object_list


class BookDeleteView(DeleteView):
    model = Book

    def get_success_url(self):
        return reverse('book-search')


class BookMarkReadView(UpdateView):
    model = Book
    form_class = BookMarkReadForm
    template_name = 'home_lib/book_mark.html'

    def post(self, request, *args, **kwargs):
        super().post(self, request, *args, **kwargs)
        obj = self.model.objects.get(pk=self.kwargs.get('pk'))
        obj.read = not obj.read
        obj.save()
        return redirect('book-search')

    def get_success_url(self):
        return reverse('book-search')


class BookWishlistView(CreateView):
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


# def stats(request):
#     from bokeh.plotting import figure
#     from bokeh.embed import components
#     from bokeh.resources import CDN
#     from bokeh.models import SingleIntervalTicker
#     from bokeh.models import Span
#
#     # 1st plot ##############################################################################
#     data_dict = AllBooks.stats()
#     all_books = data_dict['all_books']
#     print('Allbooks', all_books)
#     books_by_lang = data_dict['books_by_lang']
#
#     if request.method == "POST":
#         if request.form["monthly_goal"]:
#             monthly_goal = int(request.form["monthly_goal"])
#             max_y_ax = monthly_goal
#     else:
#         monthly_goal = 2
#         max_y_ax = None
#
#     if all_books != 0:
#         x = [i[0] for i in books_by_lang]
#         y = [i[1] for i in books_by_lang]
#
#         # Add a plot
#         p = figure(
#             title='Number of books in given languages in the collection',
#             x_range=x,
#             y_range=(0, max(y)),
#             x_axis_label='Language',
#             y_axis_label='Number of books',
#         )
#
#         p.vbar(
#             x,
#             top=y,
#             width=0.5,
#             color='green',
#             fill_alpha=0.5
#         )
#
#         script1, div1 = components(p)
#         cdn_js = CDN.js_files[0]
#
#         return render("stats.html", script1=script1, div1=div1, cdn_js=cdn_js)
