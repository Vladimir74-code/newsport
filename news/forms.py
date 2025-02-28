from django import forms
from .models import News, Author

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'author']  # Поле 'type' исключено
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
        }

class AuthorProfileForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['ratingAuthor']  # Поле, которое можно редактировать (например, рейтинг)
        widgets = {
            'ratingAuthor': forms.NumberInput(attrs={'class': 'form-control'}),
        }