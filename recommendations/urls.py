from django.urls import path
from . import views

urlpatterns = [
    path('', views.recommendation_list, name='recommendation_list'),
    path('<int:id>/read/', views.mark_read, name='mark_read'),
]