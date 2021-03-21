from django.urls import path
from charts import views

urlpatterns = [
    path('statistics', views.StatsView.as_view(), name='stats'),
    path('chart/total', views.TotalBooksChartView.as_view(), name='chart-total'),
    path('chart/total-read', views.TotalReadBooksChartView.as_view(), name='chart-total-read'),
    path('chart/reading-timeline', views.ReadingTimelineChartView.as_view(), name='chart-reading-timeline'),

]
