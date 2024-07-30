from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View
from django.contrib.auth.decorators import login_required
from .models import Post, Category, Author, Subscription, Comment
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from .filters import PostFilter
from .forms import PostForm
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.cache import cache
from django.utils.translation import gettext as _


def post_del(request, pk):
    post = Post.objects.get(pk=pk)
    return render(request, 'Newspk.html', {'post': post})


class PostList(ListView):
    model = Post
    ordering = 'author'
    template_name = 'News.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'Newspk.html'
    context_object_name = 'post'
    queryset = Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        categories = []
        for category in self.object.category.all():
            is_subscribed = self.request.user.subscription_set.filter(
                category=category).exists() if self.request.user.is_authenticated else False
            categories.append({'category': category, 'is_subscribed': is_subscribed})
        context['categories'] = categories
        return context

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}',
                        None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj


class PostSearch(ListView):
    model = Post
    ordering = 'author'
    template_name = 'search.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
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
        author = Author.objects.get(user=self.request.user)
        post.author = author
        post.save()
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


def subscribe_to_category(request, category_id):
    category = Category.objects.get(id=category_id)
    if request.method == 'GET':
        if not Subscription.objects.filter(user=request.user, category=category).exists():
            Subscription.objects.create(user=request.user, category=category)
            current_url = request.META.get('HTTP_REFERER')
            return redirect(current_url)
    return redirect(current_url)


@login_required
def comment_form_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        comment_text = request.POST.get('comment')
        new_comment = Comment(text=comment_text, post=post, user=request.user)
        new_comment.save()
        return redirect('post_detail', pk=pk)
    return render(request, 'comment_form.html', {'post': post})


def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.rating += 1
        post.save()
        return redirect('post_detail', pk=pk)
    return redirect('post_detail', pk=pk)


def dislike_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.rating -= 1
        post.save()
        return redirect('post_detail', pk=pk)
    return redirect('post_detail', pk=pk)


def like_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == 'POST':
        comment.rating += 1
        comment.save()
        current_url = request.META.get('HTTP_REFERER')
        return redirect(current_url)
    return redirect(current_url)


def dislike_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == 'POST':
        comment.rating -= 1
        comment.save()
        current_url = request.META.get('HTTP_REFERER')
        return redirect(current_url)
    return redirect(current_url)


