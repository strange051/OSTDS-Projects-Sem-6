from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('histogram/', views.histogram_view, name='histogram'),
    path('pie-chart/', views.pie_chart_view, name='pie_chart'),
    path('bar-chart/', views.bar_chart_view, name='bar_chart'),
    path('area_chart/', views.area_chart_view, name='area_chart'),
]
