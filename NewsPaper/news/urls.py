from django.urls import path
# Импортируем созданное нами представление
from .views import (PostList, PostDetail, PostSearch, NewsCreate,
                    NewsUpdate, NewsDelete, ArticleCreate, ArticleEdit, ArticleDelete, upgrade_me, subscribe_to_category, comment_form_view )
from django.views.decorators.cache import cache_page
from. import views
urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail', ),
    path('search/', PostSearch.as_view(), name='search_post'),
    path('create/', NewsCreate.as_view(), name='CreateNews'),
    path('<int:pk>/edit/', NewsUpdate.as_view(), name='EditNews'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='DeleteNews'),
    path('article/create/', ArticleCreate.as_view(), name='CreateArticle'),
    path('<int:pk>/article/edit/', ArticleEdit.as_view(), name='EditArticle'),
    path('<int:pk>/article/delete/', ArticleDelete.as_view(), name='DeleteArticle'),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('categories/<int:category_id>/subscribe/', subscribe_to_category, name='subscribe_to_category'),
    path('<int:pk>/comment/', views.comment_form_view, name='comment_form'),
    path('<int:pk>/like_post/', views.like_post, name='like_post'),
    path('<int:pk>/dislike_post', views.dislike_post, name='dislike_post'),
    path('<int:pk>/like_comment', views.like_comment, name='like_comment'),
    path('<int:pk>/dislike_comment', views.dislike_comment, name='dislike_comment'),



]
