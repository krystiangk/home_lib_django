from django.urls import path
from charts import views

app_name = 'chart'

urlpatterns = [
    path('statistics', views.StatsView.as_view(), name='stats'),
    path('total', views.TotalBooksChartView.as_view(), name='chart-total'),
    path('total-read', views.TotalReadBooksChartView.as_view(), name='chart-total-read'),
    path('reading-timeline', views.ReadingTimelineChartView.as_view(), name='chart-reading-timeline'),

]
