from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import Post, Category, Author
from django.contrib.auth.models import User


@receiver(post_save, sender=Post)
def send_newsletter(sender, instance, created, **kwargs):
    if created:
        category = instance.category
        subscribers = category.subscribers.all()
        for subscriber in subscribers:
            subject = instance.header
            message = f'Здравствуй, {subscriber.username}. Новая статья в твоём любимом разделе!'
            send_mail(subject, message, 'sobetskyvladimir@yandex.ru', [subscriber.email], )

