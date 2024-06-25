from django.contrib.sites.shortcuts import get_current_site
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail, EmailMultiAlternatives
from django.http import HttpRequest
from django.template.loader import render_to_string
from .models import Post, Subscription
from django.urls import reverse
from django.contrib.auth.models import User


@receiver(m2m_changed, sender=Post.category.through, )
def send_newsletter(sender, instance, action, **kwargs):
    if action == 'post_add':
        categories = instance.category.all()
        for category in categories:
            subscriptions = Subscription.objects.filter(category=category)
            for subscription in subscriptions:
                user = subscription.user
                subject = instance.header
                request = kwargs.get('request')
                if not request:
                    request = HttpRequest()
                current_site = get_current_site(None)
                post_url = 'https://' + current_site.domain + reverse('post_detail', args=[instance.pk])
                html_content = render_to_string('send_mail_to_sub.html',
                                                {'user': user, 'post': instance, 'post_url': post_url})
                body = instance.text
                msg = EmailMultiAlternatives(subject, body, 'sobetskyvladimir@yandex.ru', [user.email])
                msg.attach_alternative(html_content, "text/html")
                msg.send()


@receiver(post_save, sender=User)
def welcome_email(sender, instance, created, **kwargs):
    if created:
        subject = 'Регистрация на сайте News Portal прошла успешно!'
        message = f"Добро пожаловать на сайт, {instance.username}! " \
                  f"Здесь ты найдёшь очень много различных новостей и статей! " \
                  f"Переходи на сайт уже быстрее по этой ссылке " \
                  f"http://127.0.0.1:8000/News/"
        from_email = 'sobetskyvladimir@yandex.ru'
        recipient_list = [instance.email]
        send_mail(subject, message, from_email, recipient_list)
