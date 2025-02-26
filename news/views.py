from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .filters import NewsFilter
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import News
from .forms import NewsForm

def about(request):
    return render(request, 'about.html')

def news_list(request):
    news_list = News.objects.all().order_by('-published_date')
    paginator = Paginator(news_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'news_list.html', {'page_obj': page_obj})

def news_detail(request, pk):
    news = get_object_or_404(News, pk=pk)
    return render(request, 'news/news_detail.html', {'news': news})

def news_search(request):
    news_list = News.objects.all()
    filter = NewsFilter(request.GET, queryset=news_list)
    paginator = Paginator(filter.qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'news/news_search.html', {'filter': filter, 'page_obj': page_obj})

class NewsCreateView(CreateView):
    model = News
    form_class = NewsForm
    template_name = 'news/news_create.html'
    success_url = reverse_lazy('news:news_list')

    def form_valid(self, form):
        form.instance.type = 'news'
        return super().form_valid(form)

class ArticleCreateView(CreateView):
    model = News
    form_class = NewsForm
    template_name = 'news/article_create.html'
    success_url = reverse_lazy('news:news_list')

    def form_valid(self, form):
        form.instance.type = 'article'
        return super().form_valid(form)

class NewsUpdateView(UpdateView):
    model = News
    form_class = NewsForm
    template_name = 'news/news_edit.html'
    success_url = reverse_lazy('news:news_list')

class NewsDeleteView(DeleteView):
    model = News
    template_name = 'news/news_delete.html'
    success_url = reverse_lazy('news:news_list')




