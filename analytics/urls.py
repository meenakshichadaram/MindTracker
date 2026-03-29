from django.urls import path
from . import views

urlpatterns = [
    path('summary/', views.analytics_summary, name='analytics_summary'),
    path('weekly/', views.weekly_report, name='weekly_report'),
    path('heatmap/', views.mood_heatmap, name='mood_heatmap'),
]

