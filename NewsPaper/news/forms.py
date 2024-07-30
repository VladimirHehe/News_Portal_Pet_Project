from django import forms
from .models import Post, Category, Comment, Author
from django.core.exceptions import ValidationError
from .censor_by_froms import bad_words_list
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django.core.mail import send_mail, EmailMultiAlternatives
import logging


class PostForm(forms.ModelForm):
    header = forms.CharField(label="Header", max_length=120)

    class Meta:
        model = Post
        fields = ['header', 'text', 'category']

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("text")
        header = cleaned_data.get("header")
        list_word = []
        for word in text.split() and header.split():
            if word.upper() in bad_words_list:
                list_word.append(word)

        if list_word:
            raise ValidationError(
                f"Текст содержит запрещенные слова: {', '.join(list_word)}"
            )

        return cleaned_data


class CommonSignupForm(SignupForm):
    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user
