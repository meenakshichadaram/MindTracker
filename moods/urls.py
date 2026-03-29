from django.urls import path
from . import views

urlpatterns = [
    path('', views.mood_list, name='mood_list'),
    path('<int:id>/', views.mood_detail, name='mood_detail'),
    path('tags/', views.tag_list, name='tag_list'),
]