from django.urls import path
from . import views

urlpatterns = [
    path('news/', views.news_list, name='news_list'),
    path('', views.news_list, name='news_list'),  # Главная страница новостей
    path('<int:article_id>/', views.news_detail, name='news_detail'),  # Детальная страница новости
    path('about/', views.about, name='about'),  # Страница "О нас"
]