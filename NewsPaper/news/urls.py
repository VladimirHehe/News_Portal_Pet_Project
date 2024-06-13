from django.urls import path
# Импортируем созданное нами представление
from .views import (PostList, PostDetail, PostSearch, NewsCreate,
                    NewsUpdate, NewsDelete, ArticleCreate, ArticleEdit, ArticleDelete, upgrade_me, subscribe_to_category)
from . import views
urlpatterns = [
    # path — означает путь.
    # В данном случае путь ко всем товарам у нас останется пустым,
    # чуть позже станет ясно почему.
    # Т.к. наше объявленное представление является классом,
    # а Django ожидает функцию, нам надо представить этот класс в виде view.
    # Для этого вызываем метод as_view.
    path('', PostList.as_view(), name='post_list'),
    # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
    # int — указывает на то, что принимаются только целочисленные значения
    path('<int:pk>', PostDetail.as_view(), name='post_detail', ),
    path('search/', PostSearch.as_view(), name='search_post'),
    path('create/', NewsCreate.as_view(), name='CreateNews'),
    path('<int:pk>/edit/', NewsUpdate.as_view(), name='EditNews'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='DeleteNews'),
    path('article/create/', ArticleCreate.as_view(), name='CreateArticle'),
    path('<int:pk>/article/edit/', ArticleEdit.as_view(), name='EditArticle'),
    path('<int:pk>/article/delete/', ArticleDelete.as_view(), name='DeleteArticle'),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('categories/<str:category_name>/subscribe/', subscribe_to_category, name='subscribe_to_category'),
]
