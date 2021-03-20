from django.urls import path
from charts import views

urlpatterns = [
    path('total', views.TotalBooksChartView.as_view(), name='chart'),
]
