from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from .models import Post
from django.shortcuts import render
from django.urls import reverse_lazy
from .filters import PostFilter
from .forms import PostForm


def post_del(request, pk):
    post = Post.objects.get(pk=pk)
    return render(request, 'Newspk.html', {'post': post})


class PostList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = 'author'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'News.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'posts'
    paginate_by = 10


class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — product.html
    template_name = 'Newspk.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'post'


class PostSearch(ListView):
    model = Post
    ordering = 'author'
    template_name = 'search.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'create_news.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.choice = True
        return super().form_valid(form)


class NewsUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'create_news.html'


class NewsDelete(DeleteView):
    model = Post
    template_name = 'delete_news.html'
    success_url = reverse_lazy('post_list')


class ArticleCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'create_article.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.choice = False
        return super().form_valid(form)


class ArticleEdit(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'create_article.html'


class ArticleDelete(DeleteView):
    model = Post
    template_name = 'delete_article.html'
    success_url = reverse_lazy('post_list')
