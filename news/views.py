from django.shortcuts import render, get_object_or_404
from .models import Article

def about(request):
    return render(request, 'about.html')

def news_list(request):
    articles = Article.objects.all()
    return render(request, 'news/news_list.html', {'articles': articles})

def news_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    return render(request, 'news/news_detail.html', {'article': article})