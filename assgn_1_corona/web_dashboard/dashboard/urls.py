from django.urls import path
from dashboard.views import index, histogram_view, correlation_view, time_series_view, bar_chart_view, pie_chart_view, box_plot_view

urlpatterns = [
    path('', index, name='index'),
    path('histogram/', histogram_view, name='histogram'),
    path('correlation/', correlation_view, name='correlation'),
    path('time_series/', time_series_view, name='time_series'),
    path('bar_chart/', bar_chart_view, name='bar_chart'),
    path('pie_chart/', pie_chart_view, name='pie_chart'),
    path('box_plot/', box_plot_view, name='box_plot'),
]
