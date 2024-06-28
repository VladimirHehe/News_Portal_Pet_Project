from datetime import datetime, timedelta
from celery import shared_task
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives, send_mail
from django.http import HttpRequest
from django.urls import reverse
from django.template.loader import render_to_string
from .models import Post, Category, Subscription
from django.contrib.auth.models import User


@shared_task
def send_mail_week():
    categories = Category.objects.filter(subscription__isnull=False).distinct()

    for category in categories:
        new_posts = Post.objects.filter(category=category, date_created__gte=datetime.now() - timedelta(days=7))
        subscriptions = Subscription.objects.filter(category=category)
        subscribers = [subscription.user for subscription in subscriptions]

        subject = f"Привет, в твоей любимой категории есть несколько обновлений!"
        text_content = render_to_string("weekly_digest.txt", {"new_posts": new_posts, "category": category})
        html_content = render_to_string("weekly_digest.html", {"new_posts": new_posts, "category": category})

        for subscriber in subscribers:
            msg = EmailMultiAlternatives(subject, text_content, 'sobetskyvladimir@yandex.ru', [subscriber.email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()


@shared_task
def send_newsletter_task(post_id, user_id, category_id):
    post = Post.objects.get(pk=post_id)
    user = User.objects.get(pk=user_id)
    category = Category.objects.get(pk=category_id)
    subject = post.header
    current_site = Site.objects.get_current()
    post_url = 'http://' + current_site.domain + reverse('post_detail', args=[post.pk])
    html_content = render_to_string('send_mail_to_sub.html',
                                    {'user': user, 'post': post, 'post_url': post_url})
    body = post.text
    msg = EmailMultiAlternatives(subject, body, 'sobetskyvladimir@yandex.ru', [user.email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@shared_task
def welcome_email_task(user_id):
    user = User.objects.get(pk=user_id)
    subject = 'Регистрация на сайте News Portal прошла успешно!'
    message = f"Добро пожаловать на сайт, {user.username}! " \
              f"Здесь ты найдёшь очень много различных новостей и статей! " \
              f"Переходи на сайт уже быстрее по этой ссылке " \
              f"http://127.0.0.1:8000/News/"
    from_email = 'sobetskyvladimir@yandex.ru'
    send_mail(subject, message, from_email, [user.email])
