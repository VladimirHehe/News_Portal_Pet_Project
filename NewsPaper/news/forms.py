from django import forms


from .models import Post
from django.core.exceptions import ValidationError
from .censor_by_froms import bad_words_list


class PostForm(forms.ModelForm):
    header = forms.CharField(label="Заголовок", max_length=120)

    class Meta:
        model = Post
        fields = ['header', 'text', 'author', 'category']

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
