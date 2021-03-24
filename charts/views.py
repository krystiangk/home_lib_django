from django.shortcuts import render
from django.views.generic import TemplateView
from home_lib.models import Book
from django.db.models import Count, Sum
from django.contrib.auth.mixins import LoginRequiredMixin
import pandas as pd
import datetime


class TotalBooksChartView(LoginRequiredMixin, TemplateView):
    template_name = 'charts/chart_total_books.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #Problem of grouping automatically by 'id' column was solved by resetting order_by
        # which was specified in the Model.
        #https://docs.djangoproject.com/en/3.1/topics/db/aggregation/#interaction-with-default-ordering-or-order-by
        context['qs'] = Book.objects.filter(created_by=self.request.user).values('language').annotate(count=Count('language')).order_by()
        #Alternative raw SQL query
        #context['qs'] = Book.objects.raw("SELECT 1 as id, language, COUNT(language) FROM home_lib_book GROUP BY language;")

        # Sidebar flag added to change rendering of template messages, to not allow the
        # sidebar to be pushed down by alert messages. Logic implemented in 'base.html'
        context['sidebar'] = 1
        return context


class StatsView(LoginRequiredMixin, TemplateView):
    template_name = 'charts/statistics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Sidebar flag added to change rendering of template messages, to not allow the
        # sidebar to be pushed down by alert messages. Logic implemented in 'base.html'
        context['sidebar'] = 1
        return context


class TotalReadBooksChartView(LoginRequiredMixin, TemplateView):
    template_name = 'charts/chart_total_read_books.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['qs'] = Book.objects.filter(read=True).filter(created_by=self.request.user).values('language').annotate(count=Count('language')).order_by()

        # Sidebar flag added to change rendering of template messages, to not allow the
        # sidebar to be pushed down by alert messages. Logic implemented in 'base.html'
        context['sidebar'] = 1

        return context


class ReadingTimelineChartView(LoginRequiredMixin, TemplateView):
    template_name = 'charts/chart_reading_timeline.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['qs'] = Book.objects.filter(read=True).filter(created_by=self.request.user).values_list('read_timestamp__year', 'read_timestamp__month')\
            .annotate(count=Count('read_timestamp')).order_by('read_timestamp__year', 'read_timestamp__month')

        # Creating a dict of tuples with ((year,month), value) format
        reading_timeline = dict([((obj[1], obj[0]), obj[2]) for obj in context['qs']])
        half_year_period = [tuple([obj.month, obj.year]) for obj in pd.period_range(end=datetime.datetime.now(),
                                                                                    freq="M", periods=6).to_list()]
        context['qs'] = []
        for date in half_year_period:
            print(date)
            if reading_timeline.get(date):
                context['qs'].append(date + (reading_timeline[date],))
            else:
                context['qs'].append(date + (0,))

        # Sidebar flag added to change rendering of template messages, to not allow the
        # sidebar to be pushed down by alert messages. Logic implemented in 'base.html'
        context['sidebar'] = 1

        return context


