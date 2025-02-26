from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    def update_rating(self):
        postRat = self.news_set.aggregate(postRating=Sum('rating'))  # Изменено с post_set на news_set
        pRat = postRat.get('postRating', 0) or 0
        commentRat = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))
        cRat = commentRat.get('commentRating', 0) or 0
        self.ratingAuthor = pRat * 3 + cRat
        self.save()

class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

class News(models.Model):
    TYPE_CHOICES = [
        ('news', 'Новость'),
        ('article', 'Статья'),
    ]
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание')
    published_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Автор')  # Изменено на ForeignKey
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='news', verbose_name='Тип')
    rating = models.SmallIntegerField(default=0)  # Добавлено из Post
    categories = models.ManyToManyField(Category, through='NewsCategory', blank=True)  # Добавлено из Post

    def __str__(self): return self.title

    def like(self): self.rating += 1; self.save()
    def dislike(self): self.rating -= 1; self.save()
    def preview(self): return f'{self.content[:124]}...'

    class Meta:
        ordering = ['-published_date']
        verbose_name = 'Новость/Статья'
        verbose_name_plural = 'Новости/Статьи'

class NewsCategory(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    commentPost = models.ForeignKey(News, on_delete=models.CASCADE)  # Изменено с Post на News
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def __str__(self): return self.commentUser.username
    def like(self): self.rating += 1; self.save()
    def dislike(self): self.rating -= 1; self.save()
    def post_com(self): return f'Комментарий к статье:\n Дата: {self.dateCreation}\nПользователь: {self.commentUser}\n Рейтинг: {self.rating}\n Комментарий: {self.text}'