from django.forms import DateInput
from django_filters import FilterSet, CharFilter, ModelChoiceFilter, DateFilter

from .models import Post, Author, User


class PostFilter(FilterSet):
    author = ModelChoiceFilter(
        queryset=Author.objects.all(),
        label="Автор",
        empty_label="Все авторы")

    text = CharFilter(lookup_expr='icontains',
                      label="Содержание",
                      )

    date_created = DateFilter(lookup_expr='gte',
                              field_name='date_created',
                              label="Показать после даты:",
                              widget=DateInput(attrs={'type': 'date'})
                              )

    class Meta:
        model = Post
        fields = ['author', 'text', 'date_created', ]
