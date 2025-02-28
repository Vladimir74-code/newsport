from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .filters import NewsFilter
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import News, Author
from .forms import NewsForm, AuthorProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import Group

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

class NewsCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'news.add_news'
    permission_denied_message = 'У вас нет прав для создания новостей.'
    raise_exception = False
    login_url = '/accounts/login/'
    redirect_field_name = 'next'
    model = News
    form_class = NewsForm
    template_name = 'news/news_create.html'
    success_url = reverse_lazy('news:news_list')

    def form_valid(self, form):
        form.instance.type = 'news'
        return super().form_valid(form)

class ArticleCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'news.add_news'
    permission_denied_message = 'У вас нет прав для создания статей.'
    raise_exception = False
    login_url = '/accounts/login/'
    redirect_field_name = 'next'
    model = News
    form_class = NewsForm
    template_name = 'news/article_create.html'
    success_url = reverse_lazy('news:news_list')

    def form_valid(self, form):
        form.instance.type = 'article'
        return super().form_valid(form)

class NewsUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'news.change_news'
    permission_denied_message = 'У вас нет прав для редактирования записей.'
    raise_exception = False
    login_url = '/accounts/login/'
    redirect_field_name = 'next'
    model = News
    form_class = NewsForm
    template_name = 'news/news_edit.html'
    success_url = reverse_lazy('news:news_list')

class NewsDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'news.delete_news'
    permission_denied_message = 'У вас нет прав для удаления записей.'
    raise_exception = False
    login_url = '/accounts/login/'
    redirect_field_name = 'next'
    model = News
    template_name = 'news/news_delete.html'
    success_url = reverse_lazy('news:news_list')

class AuthorProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Author
    form_class = AuthorProfileForm
    template_name = 'news/author_profile_edit.html'
    success_url = reverse_lazy('news:news_list')

    def get_object(self, queryset=None):
        return self.request.user.author

@login_required
def become_author(request):
    if request.user.groups.filter(name='authors').exists():
        messages.info(request, 'Вы уже являетесь автором.')
        return redirect('news:news_list')
    try:
        author_group = Group.objects.get(name='authors')
    except Group.DoesNotExist:
        author_group = Group.objects.create(name='authors')
    request.user.groups.add(author_group)
    Author.objects.get_or_create(authorUser=request.user)
    messages.success(request, 'Вы успешно стали автором!')
    return redirect('news:news_list')




