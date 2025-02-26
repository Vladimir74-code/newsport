from django.urls import path
from . import views
from .views import NewsCreateView, ArticleCreateView, NewsUpdateView, NewsDeleteView

app_name = 'news'

urlpatterns = [
    path('', views.news_list, name='news_list'),
    path('about/', views.about, name='about'),
    path('search/', views.news_search, name='news_search'),
    path('news/create/', NewsCreateView.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', NewsUpdateView.as_view(), name='news_edit'),
    path('news/<int:pk>/delete/', NewsDeleteView.as_view(), name='news_delete'),
    path('articles/create/', ArticleCreateView.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', NewsUpdateView.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', NewsDeleteView.as_view(), name='article_delete'),
    path('<int:pk>/', views.news_detail, name='news_detail'),
]
