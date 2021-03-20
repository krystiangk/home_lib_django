from django.shortcuts import render
from django.views.generic import TemplateView
from home_lib.models import Book
from django.db.models import Count, Sum


class TotalBooksChartView(TemplateView):
    template_name = 'charts/chart_total_books.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #Problem of grouping automatically by 'id' column was solved by resetting order_by
        # which was specified in the Model.
        #https://docs.djangoproject.com/en/3.1/topics/db/aggregation/#interaction-with-default-ordering-or-order-by
        context['qs'] = Book.objects.values('language').annotate(count=Count('language')).order_by()
        #Alternative raw SQL query
        #context['qs'] = Book.objects.raw("SELECT 1 as id, language, COUNT(language) FROM home_lib_book GROUP BY language;")
        print(context['qs'])
        print(context['qs'].query)

        return context