from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View
from django.contrib.auth.decorators import login_required
from .models import Post, Category, PostCategory, Author
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from .filters import PostFilter
from .forms import PostForm
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — product.html
    template_name = 'Newspk.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


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
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class NewsCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'create_news.html'
    permission_required = 'news.add_post'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.choice = True
        return super().form_valid(form)


class NewsUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'create_news.html'
    permission_required = 'news.change_post'


class NewsDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'delete_news.html'
    success_url = reverse_lazy('post_list')
    permission_required = 'news.delete_post'


class ArticleCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'create_article.html'
    permission_required = 'news.add_post'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.choice = False
        return super().form_valid(form)


class ArticleEdit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'create_article.html'
    permission_required = 'news.change_post'


class ArticleDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'delete_article.html'
    success_url = reverse_lazy('post_list')
    permission_required = 'news.delete_post'


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
        Author.objects.create(user=user)
    return redirect('post_list')


@login_required
def subscribe_to_category(request, category_id):
    category = Category.objects.get(id=category_id)
    if request.method == 'POST':
        if not request.user in category.subscribers.all():
            category.subscribers.add(request.user)
            return redirect('post_list')
    return redirect('post_list')
